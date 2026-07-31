import {
  createHmac,
  pbkdf2Sync,
  randomBytes,
  timingSafeEqual,
} from "node:crypto";
import { neon } from "@neondatabase/serverless";

const DATABASE_URL = process.env.DATABASE_URL || "";
const SESSION_SECRET = process.env.ADMIN_SESSION_SECRET || "";
const INITIAL_PASSWORD = process.env.ADMIN_INITIAL_PASSWORD || "";
const TOKEN_TTL_SECONDS = 12 * 60 * 60;
const PBKDF2_ITERATIONS = 240_000;
const MAX_IMAGE_BYTES = 3_500_000;
const MAX_CONTENT_BYTES = 600_000;
const MAX_REQUEST_BYTES = 5_000_000;
const LOGIN_WINDOW_MINUTES = 15;
const LOGIN_MAX_FAILURES = 5;

const sql = DATABASE_URL ? neon(DATABASE_URL) : null;
let schemaReady;

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

function hashPassword(password) {
  const salt = randomBytes(16).toString("hex");
  const digest = pbkdf2Sync(password, Buffer.from(salt, "hex"), PBKDF2_ITERATIONS, 32, "sha256");
  return `pbkdf2$${salt}$${digest.toString("hex")}`;
}

function verifyPassword(password, stored) {
  try {
    const [kind, salt, expectedHex] = String(stored).split("$");
    if (kind !== "pbkdf2" || !salt || !expectedHex) return false;
    const actual = pbkdf2Sync(password, Buffer.from(salt, "hex"), PBKDF2_ITERATIONS, 32, "sha256");
    const expected = Buffer.from(expectedHex, "hex");
    return actual.length === expected.length && timingSafeEqual(actual, expected);
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

function makeToken(passwordHash) {
  const expiry = String(Math.floor(Date.now() / 1000) + TOKEN_TTL_SECONDS);
  const passwordVersion = createHmac("sha256", SESSION_SECRET)
    .update(String(passwordHash))
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
      timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
    if (!signatureValid) return false;
    const rows = await sql`SELECT password_hash FROM admin_settings WHERE id = 1`;
    if (!rows.length) return false;
    const currentVersion = createHmac("sha256", SESSION_SECRET)
      .update(String(rows[0].password_hash))
      .digest("hex")
      .slice(0, 24);
    return (
      passwordVersion.length === currentVersion.length &&
      timingSafeEqual(Buffer.from(passwordVersion), Buffer.from(currentVersion))
    );
  } catch {
    return false;
  }
}

function requestIp(event) {
  const headers = event.headers || {};
  return String(
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
          password_hash TEXT NOT NULL,
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
      `;
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
  const unsafeImage = [...content.products, ...content.gallery].some(
    (item) => item && !validImageUrl(item.imageUrl)
  );
  if (unsafeImage) return "Image URLs must use HTTPS or a secure uploaded image.";
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
  let rows = await sql`SELECT password_hash FROM admin_settings WHERE id = 1`;
  if (!rows.length) {
    if (!INITIAL_PASSWORD || !passwordMeetsPolicy(INITIAL_PASSWORD)) {
      return json(503, {
        ok: false,
        error: "Admin login is not initialized. Set ADMIN_INITIAL_PASSWORD in Netlify.",
      });
    }
    await sql`
      INSERT INTO admin_settings (id, password_hash)
      VALUES (1, ${hashPassword(INITIAL_PASSWORD)})
      ON CONFLICT (id) DO NOTHING
    `;
    rows = await sql`SELECT password_hash FROM admin_settings WHERE id = 1`;
  }
  if (!rows.length || !verifyPassword(password, rows[0].password_hash)) {
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
    return json(401, { ok: false, error: "Wrong password." });
  }
  await sql`DELETE FROM admin_login_attempts WHERE client_hash = ${ipHash}`;
  return json(200, { ok: true, token: makeToken(rows[0].password_hash) });
}

async function changePassword(body) {
  if (!(await requireToken(body))) return json(401, { ok: false, error: "Session expired. Log in again." });
  if (!passwordMeetsPolicy(body.new_password)) {
    return json(400, {
      ok: false,
      error: "Use at least 8 characters with uppercase, lowercase, a number and a special symbol.",
    });
  }
  const rows = await sql`SELECT password_hash FROM admin_settings WHERE id = 1`;
  if (!rows.length || !verifyPassword(String(body.current_password || ""), rows[0].password_hash)) {
    return json(401, { ok: false, error: "Current password is wrong." });
  }
  const newHash = hashPassword(body.new_password);
  await sql`
    UPDATE admin_settings
    SET password_hash = ${newHash}, updated_at = now()
    WHERE id = 1
  `;
  return json(200, { ok: true, token: makeToken(newHash) });
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
