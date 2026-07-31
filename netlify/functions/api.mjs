import {
  createHmac,
  randomBytes,
} from "node:crypto";
import { neon } from "@neondatabase/serverless";

let DATABASE_URL = "";
let SESSION_SECRET = "";
let INITIAL_PASSWORD = "";
let INITIAL_USERNAME = "admin";
const TOKEN_TTL_SECONDS = 12 * 60 * 60;
const PBKDF2_ITERATIONS = 240_000;
const MAX_IMAGE_BYTES = 3_500_000;
const MAX_CONTENT_BYTES = 600_000;
const MAX_REQUEST_BYTES = 5_000_000;
const LOGIN_WINDOW_MINUTES = 15;
const LOGIN_MAX_FAILURES = 5;

let sql = null;
let schemaReady;

function configureRuntime(event) {
  const runtime = event && event.env ? event.env : process.env;
  const nextDatabaseUrl = runtime.DATABASE_URL || process.env.DATABASE_URL || "";
  if (nextDatabaseUrl !== DATABASE_URL) {
    DATABASE_URL = nextDatabaseUrl;
    sql = DATABASE_URL ? neon(DATABASE_URL) : null;
    schemaReady = undefined;
  }
  SESSION_SECRET =
    runtime.ADMIN_SESSION_SECRET || process.env.ADMIN_SESSION_SECRET || "";
  INITIAL_PASSWORD =
    runtime.ADMIN_INITIAL_PASSWORD || process.env.ADMIN_INITIAL_PASSWORD || "";
  INITIAL_USERNAME =
    runtime.ADMIN_INITIAL_USERNAME || process.env.ADMIN_INITIAL_USERNAME || "admin";
}

const headers = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "Referrer-Policy": "no-referrer",
};

function json(statusCode, value, extraHeaders = {}) {
  return {
    statusCode,
    headers: { ...headers, ...extraHeaders },
    body: JSON.stringify(value),
  };
}

function routePath(event) {
  const path = new URL(event.rawUrl || `https://local${event.path || "/"}`).pathname;
  return path.replace(/^\/\.netlify\/functions\/api/, "/api");
}

function parseBody(event) {
  if (!event.body) return {};
  if (Buffer.byteLength(event.body, "utf8") > MAX_REQUEST_BYTES) return undefined;
  try {
    return JSON.parse(event.body);
  } catch {
    return null;
  }
}

function bytesToHex(bytes) {
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("");
}

function secureEqual(left, right) {
  const encoder = new TextEncoder();
  const leftBytes = typeof left === "string" ? encoder.encode(left) : left;
  const rightBytes = typeof right === "string" ? encoder.encode(right) : right;
  if (leftBytes.length !== rightBytes.length) return false;
  let difference = 0;
  for (let index = 0; index < leftBytes.length; index += 1) {
    difference |= leftBytes[index] ^ rightBytes[index];
  }
  return difference === 0;
}

function hexToBytes(hex) {
  if (!/^[a-f0-9]+$/i.test(hex) || hex.length % 2) throw new Error("Invalid hex");
  return Uint8Array.from(hex.match(/.{2}/g), (pair) => Number.parseInt(pair, 16));
}

async function derivePassword(password, salt) {
  const key = await globalThis.crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(password),
    "PBKDF2",
    false,
    ["deriveBits"]
  );
  const bits = await globalThis.crypto.subtle.deriveBits(
    { name: "PBKDF2", hash: "SHA-256", salt, iterations: PBKDF2_ITERATIONS },
    key,
    256
  );
  return new Uint8Array(bits);
}

async function hashPassword(password) {
  const salt = globalThis.crypto.getRandomValues(new Uint8Array(16));
  const digest = await derivePassword(password, salt);
  return `pbkdf2$${bytesToHex(salt)}$${bytesToHex(digest)}`;
}

async function verifyPassword(password, stored) {
  try {
    const [kind, salt, expectedHex] = String(stored).split("$");
    if (kind !== "pbkdf2" || !salt || !expectedHex) return false;
    const actual = await derivePassword(password, hexToBytes(salt));
    const expected = hexToBytes(expectedHex);
    return secureEqual(actual, expected);
  } catch {
    return false;
  }
}

function passwordMeetsPolicy(password) {
  return (
    typeof password === "string" &&
    password.length >= 8 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /\d/.test(password) &&
    /[^A-Za-z0-9]/.test(password)
  );
}

function makeToken(username, passwordHash) {
  const expiry = String(Math.floor(Date.now() / 1000) + TOKEN_TTL_SECONDS);
  const passwordVersion = createHmac("sha256", SESSION_SECRET)
    .update(`${username}:${passwordHash}`)
    .digest("hex")
    .slice(0, 24);
  const payload = `${expiry}.${passwordVersion}`;
  const signature = createHmac("sha256", SESSION_SECRET).update(payload).digest("hex");
  return `${payload}.${signature}`;
}

async function tokenValid(token) {
  try {
    const [expiry, passwordVersion, signature] = String(token || "").split(".");
    if (!expiry || !passwordVersion || !signature || Number(expiry) <= Date.now() / 1000) return false;
    const payload = `${expiry}.${passwordVersion}`;
    const expected = createHmac("sha256", SESSION_SECRET).update(payload).digest("hex");
    const signatureValid =
      signature.length === expected.length &&
      secureEqual(signature, expected);
    if (!signatureValid) return false;
    const rows = await sql`SELECT username, password_hash FROM admin_settings WHERE id = 1`;
    if (!rows.length) return false;
    const currentVersion = createHmac("sha256", SESSION_SECRET)
      .update(`${rows[0].username}:${rows[0].password_hash}`)
      .digest("hex")
      .slice(0, 24);
    return (
      passwordVersion.length === currentVersion.length &&
      secureEqual(passwordVersion, currentVersion)
    );
  } catch {
    return false;
  }
}

function requestIp(event) {
  const headers = event.headers || {};
  return String(
    headers["cf-connecting-ip"] ||
    headers["x-nf-client-connection-ip"] ||
    headers["client-ip"] ||
    headers["x-forwarded-for"] ||
    "unknown"
  ).split(",")[0].trim();
}

function clientHash(event) {
  return createHmac("sha256", SESSION_SECRET).update(requestIp(event)).digest("hex");
}

function sameOrigin(event) {
  const origin = String((event.headers || {}).origin || "");
  if (!origin) return true;
  try {
    const requestUrl = new URL(event.rawUrl || `https://${(event.headers || {}).host || "local"}/`);
    return new URL(origin).host === requestUrl.host;
  } catch {
    return false;
  }
}

function validImageUrl(value) {
  if (!value) return true;
  const url = String(value).trim();
  if (/^\/api\/image\/[a-f0-9]{24}\.(jpg|png)$/.test(url)) return true;
  if (
    !url.includes("..") &&
    /^\/?assets\/[A-Za-z0-9_./-]+\.(?:jpe?g|png|webp)$/i.test(url)
  ) return true;
  try {
    return new URL(url).protocol === "https:";
  } catch {
    return false;
  }
}

async function ensureSchema() {
  if (!sql) throw new Error("DATABASE_URL is not configured");
  if (!schemaReady) {
    schemaReady = (async () => {
      await sql`
        CREATE TABLE IF NOT EXISTS admin_settings (
          id SMALLINT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
          username TEXT NOT NULL DEFAULT 'admin',
          password_hash TEXT NOT NULL,
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
      `;
      await sql`ALTER TABLE admin_settings ADD COLUMN IF NOT EXISTS username TEXT NOT NULL DEFAULT 'admin'`;
      await sql`
        CREATE TABLE IF NOT EXISTS site_content (
          id SMALLINT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
          data JSONB NOT NULL DEFAULT '{}'::jsonb,
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
      `;
      await sql`
        CREATE TABLE IF NOT EXISTS images (
          id TEXT PRIMARY KEY,
          mime TEXT NOT NULL,
          data BYTEA NOT NULL,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
      `;
      await sql`
        CREATE TABLE IF NOT EXISTS admin_login_attempts (
          client_hash TEXT PRIMARY KEY,
          failures SMALLINT NOT NULL DEFAULT 0,
          window_started TIMESTAMPTZ NOT NULL DEFAULT now(),
          blocked_until TIMESTAMPTZ
        )
      `;
      await sql`
        CREATE TABLE IF NOT EXISTS geocode_cache (
          query TEXT PRIMARY KEY,
          latitude DOUBLE PRECISION NOT NULL,
          longitude DOUBLE PRECISION NOT NULL,
          display_name TEXT NOT NULL DEFAULT '',
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
      `;
      await sql`
        CREATE TABLE IF NOT EXISTS geocode_rate (
          id SMALLINT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
          last_request TIMESTAMPTZ NOT NULL DEFAULT to_timestamp(0)
        )
      `;
      await sql`INSERT INTO geocode_rate (id) VALUES (1) ON CONFLICT (id) DO NOTHING`;
    })().catch((error) => {
      schemaReady = undefined;
      throw error;
    });
  }
  return schemaReady;
}

async function requireToken(body) {
  return body && await tokenValid(body.token);
}

function validateContent(content) {
  if (!content || typeof content !== "object" || Array.isArray(content)) return "Invalid content.";
  if (Buffer.byteLength(JSON.stringify(content), "utf8") > MAX_CONTENT_BYTES) return "Content is too large.";
  if (!Array.isArray(content.products) || !Array.isArray(content.gallery)) {
    return "Products and gallery must be lists.";
  }
  if (content.products.length > 200 || content.gallery.length > 300) {
    return "Too many products or gallery entries.";
  }
  const teamMembers = ["core", "contributors", "volunteers"].flatMap(
    (key) => Array.isArray(content.team && content.team[key]) ? content.team[key] : []
  );
  const education = Array.isArray(content.educationArticles) ? content.educationArticles : [];
  const branches = Array.isArray(content.branches) ? content.branches : [];
  const impactMetrics = Array.isArray(content.impactMetrics) ? content.impactMetrics : [];
  if (teamMembers.length > 200 || education.length > 200 || branches.length > 100 || impactMetrics.length > 30) {
    return "Too many team members, education entries, or branches.";
  }
  const unsafeImage = [...content.products, ...content.gallery, ...teamMembers, ...education].some(
    (item) => item && !validImageUrl(item.imageUrl)
  );
  if (unsafeImage) return "Image URLs must use HTTPS or a secure uploaded image.";
  const externalLinks = [
    content.seller && content.seller.profileUrl,
    ...teamMembers.map((item) => item && item.profileUrl),
    ...education.map((item) => item && item.linkUrl),
  ].filter(Boolean);
  if (externalLinks.some((value) => {
    try { return new URL(String(value)).protocol !== "https:"; } catch { return true; }
  })) return "External links must use HTTPS.";
  if (branches.some((branch) => {
    const lat = Number(branch && branch.latitude);
    const lng = Number(branch && branch.longitude);
    return !Number.isFinite(lat) || !Number.isFinite(lng) || lat < -90 || lat > 90 || lng < -180 || lng > 180;
  })) return "Every branch needs valid map coordinates.";
  return "";
}

function normalizeContent(content) {
  if (!content || typeof content !== "object" || Array.isArray(content)) return content;
  const normalized = { ...content };
  if (Array.isArray(content.products)) {
    normalized.products = content.products.map((product) => ({
      ...product,
      price: String(product && product.price ? product.price : "").trim() || "Price on request",
    }));
  }
  return normalized;
}

async function login(body, event) {
  if (!SESSION_SECRET) {
    return json(503, {
      ok: false,
      error: "Admin sessions are not configured. Set ADMIN_SESSION_SECRET in Netlify.",
    });
  }
  const ipHash = clientHash(event);
  const attempts = await sql`
    SELECT failures, window_started, blocked_until
    FROM admin_login_attempts
    WHERE client_hash = ${ipHash}
  `;
  if (attempts.length && attempts[0].blocked_until && new Date(attempts[0].blocked_until) > new Date()) {
    return json(429, { ok: false, error: "Too many login attempts. Try again in 15 minutes." });
  }
  const password = String(body.password || "");
  const username = String(body.username || "admin").trim();
  let rows = await sql`SELECT username, password_hash FROM admin_settings WHERE id = 1`;
  if (!rows.length) {
    if (!INITIAL_PASSWORD || !passwordMeetsPolicy(INITIAL_PASSWORD)) {
      return json(503, {
        ok: false,
        error: "Admin login is not initialized. Set ADMIN_INITIAL_PASSWORD in Netlify.",
      });
    }
    await sql`
      INSERT INTO admin_settings (id, username, password_hash)
      VALUES (1, ${INITIAL_USERNAME}, ${await hashPassword(INITIAL_PASSWORD)})
      ON CONFLICT (id) DO NOTHING
    `;
    rows = await sql`SELECT username, password_hash FROM admin_settings WHERE id = 1`;
  }
  if (!rows.length || username !== rows[0].username || !(await verifyPassword(password, rows[0].password_hash))) {
    await sql`
      INSERT INTO admin_login_attempts (client_hash, failures, window_started, blocked_until)
      VALUES (${ipHash}, 1, now(), NULL)
      ON CONFLICT (client_hash) DO UPDATE SET
        failures = CASE
          WHEN admin_login_attempts.window_started < now() - (${LOGIN_WINDOW_MINUTES} * interval '1 minute')
            THEN 1
          ELSE admin_login_attempts.failures + 1
        END,
        window_started = CASE
          WHEN admin_login_attempts.window_started < now() - (${LOGIN_WINDOW_MINUTES} * interval '1 minute')
            THEN now()
          ELSE admin_login_attempts.window_started
        END,
        blocked_until = CASE
          WHEN (
            CASE
              WHEN admin_login_attempts.window_started < now() - (${LOGIN_WINDOW_MINUTES} * interval '1 minute')
                THEN 1
              ELSE admin_login_attempts.failures + 1
            END
          ) >= ${LOGIN_MAX_FAILURES}
            THEN now() + (${LOGIN_WINDOW_MINUTES} * interval '1 minute')
          ELSE NULL
        END
    `;
    return json(401, { ok: false, error: "Wrong username or password." });
  }
  await sql`DELETE FROM admin_login_attempts WHERE client_hash = ${ipHash}`;
  return json(200, { ok: true, token: makeToken(rows[0].username, rows[0].password_hash) });
}

async function changePassword(body) {
  if (!(await requireToken(body))) return json(401, { ok: false, error: "Session expired. Log in again." });
  if (!passwordMeetsPolicy(body.new_password)) {
    return json(400, {
      ok: false,
      error: "Use at least 8 characters with uppercase, lowercase, a number and a special symbol.",
    });
  }
  const username = String(body.username || "").trim();
  if (!/^[A-Za-z0-9._-]{3,40}$/.test(username)) {
    return json(400, { ok: false, error: "Username must be 3-40 letters, numbers, dots, dashes, or underscores." });
  }
  const rows = await sql`SELECT username, password_hash FROM admin_settings WHERE id = 1`;
  if (!rows.length || !(await verifyPassword(String(body.current_password || ""), rows[0].password_hash))) {
    return json(401, { ok: false, error: "Current password is wrong." });
  }
  const newHash = await hashPassword(body.new_password);
  await sql`
    UPDATE admin_settings
    SET username = ${username}, password_hash = ${newHash}, updated_at = now()
    WHERE id = 1
  `;
  return json(200, { ok: true, token: makeToken(username, newHash) });
}

async function geocodeAddress(body) {
  if (!(await requireToken(body))) return json(401, { ok: false, error: "Session expired. Log in again." });
  const query = String(body.address || "").trim().replace(/\s+/g, " ");
  if (query.length < 8 || query.length > 300) {
    return json(400, { ok: false, error: "Enter a complete address before locating it." });
  }
  const cacheKey = query.toLowerCase();
  const cached = await sql`
    SELECT latitude, longitude, display_name
    FROM geocode_cache
    WHERE query = ${cacheKey}
  `;
  if (cached.length) return json(200, { ok: true, ...cached[0], cached: true });
  const allowed = await sql`
    UPDATE geocode_rate
    SET last_request = now()
    WHERE id = 1 AND last_request <= now() - interval '1 second'
    RETURNING id
  `;
  if (!allowed.length) return json(429, { ok: false, error: "Please wait a moment before locating another address." });
  const endpoint = process.env.GEOCODING_BASE_URL || "https://nominatim.openstreetmap.org";
  const response = await fetch(
    `${endpoint}/search?format=jsonv2&limit=1&countrycodes=in&q=${encodeURIComponent(query)}`,
    {
      headers: {
        "User-Agent": "ReclaimEraWebsite/1.0 (reclaimera@gmail.com)",
        "Accept-Language": "en",
      },
    }
  );
  if (!response.ok) return json(502, { ok: false, error: "The map service could not locate that address." });
  const results = await response.json();
  if (!Array.isArray(results) || !results.length) {
    return json(404, { ok: false, error: "Address not found. Enter latitude and longitude manually." });
  }
  const latitude = Number(results[0].lat);
  const longitude = Number(results[0].lon);
  const displayName = String(results[0].display_name || query).slice(0, 500);
  await sql`
    INSERT INTO geocode_cache (query, latitude, longitude, display_name, updated_at)
    VALUES (${cacheKey}, ${latitude}, ${longitude}, ${displayName}, now())
    ON CONFLICT (query) DO UPDATE SET
      latitude = EXCLUDED.latitude,
      longitude = EXCLUDED.longitude,
      display_name = EXCLUDED.display_name,
      updated_at = now()
  `;
  return json(200, { ok: true, latitude, longitude, display_name: displayName, cached: false });
}

async function getContent() {
  const rows = await sql`SELECT data, updated_at FROM site_content WHERE id = 1`;
  const content = normalizeContent(rows.length && rows[0].data ? rows[0].data : {});
  return json(200, content, { "Cache-Control": "public, max-age=0, must-revalidate" });
}

async function saveContent(body) {
  if (!(await requireToken(body))) return json(401, { ok: false, error: "Session expired. Log in again." });
  const error = validateContent(body.content);
  if (error) return json(400, { ok: false, error });
  const serialized = JSON.stringify(normalizeContent(body.content));
  await sql`
    INSERT INTO site_content (id, data, updated_at)
    VALUES (1, ${serialized}::jsonb, now())
    ON CONFLICT (id)
    DO UPDATE SET data = EXCLUDED.data, updated_at = now()
  `;
  return json(200, { ok: true });
}

async function uploadImage(body) {
  if (!(await requireToken(body))) return json(401, { ok: false, error: "Session expired. Log in again." });
  const match = /^data:(image\/(png|jpe?g));base64,([A-Za-z0-9+/=\s]+)$/i.exec(String(body.data || ""));
  if (!match) return json(400, { ok: false, error: "Only JPEG or PNG images are allowed." });
  const mime = /^image\/png$/i.test(match[1]) ? "image/png" : "image/jpeg";
  const raw = Buffer.from(match[3].replace(/\s/g, ""), "base64");
  if (!raw.length || raw.length > MAX_IMAGE_BYTES) {
    return json(400, { ok: false, error: "Image is empty or larger than 3.5 MB." });
  }
  const isPng = raw.length >= 8 && raw.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]));
  const isJpeg = raw.length >= 3 && raw[0] === 0xff && raw[1] === 0xd8 && raw[2] === 0xff;
  if ((mime === "image/png" && !isPng) || (mime === "image/jpeg" && !isJpeg)) {
    return json(400, { ok: false, error: "The uploaded file does not match its image type." });
  }
  const id = `${randomBytes(12).toString("hex")}${mime === "image/png" ? ".png" : ".jpg"}`;
  await sql`
    INSERT INTO images (id, mime, data)
    VALUES (${id}, ${mime}, decode(${raw.toString("base64")}, 'base64'))
  `;
  return json(200, { ok: true, url: `/api/image/${id}` });
}

async function getImage(id) {
  if (!/^[a-f0-9]{24}\.(jpg|png)$/.test(id)) return json(404, { ok: false });
  const rows = await sql`SELECT mime, encode(data, 'base64') AS encoded FROM images WHERE id = ${id}`;
  if (!rows.length) return json(404, { ok: false });
  return {
    statusCode: 200,
    headers: {
      "Content-Type": rows[0].mime,
      "Cache-Control": "public, max-age=31536000, immutable",
      "X-Content-Type-Options": "nosniff",
    },
    body: rows[0].encoded,
    isBase64Encoded: true,
  };
}

export async function handler(event) {
  configureRuntime(event);
  if (event.httpMethod === "OPTIONS") return { statusCode: 204, headers, body: "" };
  if (!DATABASE_URL) return json(503, { ok: false, error: "DATABASE_URL is not configured." });

  try {
    await ensureSchema();
    const path = routePath(event);
    const method = event.httpMethod || "GET";
    const body = parseBody(event);
    if (body === undefined) return json(413, { ok: false, error: "Request is too large." });
    if (body === null) return json(400, { ok: false, error: "Invalid JSON." });
    if (method === "POST" && !sameOrigin(event)) {
      return json(403, { ok: false, error: "Cross-site requests are not allowed." });
    }

    if (method === "GET" && path === "/api/health") {
      await sql`SELECT 1`;
      return json(200, { ok: true, database: true });
    }
    if (method === "GET" && path === "/api/content") return getContent();
    if (method === "POST" && path === "/api/admin/login") return login(body, event);
    if (method === "POST" && path === "/api/admin/check") {
      return await tokenValid(body.token) ? json(200, { ok: true }) : json(401, { ok: false });
    }
    if (method === "POST" && path === "/api/admin/change-password") return changePassword(body);
    if (method === "POST" && path === "/api/admin/content") return saveContent(body);
    if (method === "POST" && path === "/api/admin/upload") return uploadImage(body);
    if (method === "POST" && path === "/api/admin/geocode") return geocodeAddress(body);
    if (method === "GET" && path.startsWith("/api/image/")) {
      return getImage(decodeURIComponent(path.slice("/api/image/".length)));
    }
    return json(404, { ok: false, error: "Not found." });
  } catch (error) {
    console.error("API error", error);
    return json(500, { ok: false, error: "The server could not complete this request." });
  }
}

export const config = {
  path: "/api/*",
  rateLimit: {
    windowLimit: 300,
    windowSize: 60,
    aggregateBy: ["ip", "domain"],
  },
};
