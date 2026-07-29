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

const sql = DATABASE_URL ? neon(DATABASE_URL) : null;
let schemaReady;

const headers = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
  "X-Content-Type-Options": "nosniff",
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

function makeToken() {
  const expiry = String(Math.floor(Date.now() / 1000) + TOKEN_TTL_SECONDS);
  const signature = createHmac("sha256", SESSION_SECRET).update(expiry).digest("hex");
  return `${expiry}.${signature}`;
}

function tokenValid(token) {
  try {
    const [expiry, signature] = String(token || "").split(".");
    if (!expiry || !signature || Number(expiry) <= Date.now() / 1000) return false;
    const expected = createHmac("sha256", SESSION_SECRET).update(expiry).digest("hex");
    return (
      signature.length === expected.length &&
      timingSafeEqual(Buffer.from(signature), Buffer.from(expected))
    );
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
    })().catch((error) => {
      schemaReady = undefined;
      throw error;
    });
  }
  return schemaReady;
}

async function requireToken(body) {
  return body && tokenValid(body.token);
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

async function login(body) {
  if (!SESSION_SECRET) {
    return json(503, {
      ok: false,
      error: "Admin sessions are not configured. Set ADMIN_SESSION_SECRET in Netlify.",
    });
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
    return json(401, { ok: false, error: "Wrong password." });
  }
  return json(200, { ok: true, token: makeToken() });
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
  await sql`
    UPDATE admin_settings
    SET password_hash = ${hashPassword(body.new_password)}, updated_at = now()
    WHERE id = 1
  `;
  return json(200, { ok: true });
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
    if (body === null) return json(400, { ok: false, error: "Invalid JSON." });

    if (method === "GET" && path === "/api/health") {
      await sql`SELECT 1`;
      return json(200, { ok: true, database: true });
    }
    if (method === "GET" && path === "/api/content") return getContent();
    if (method === "POST" && path === "/api/admin/login") return login(body);
    if (method === "POST" && path === "/api/admin/check") {
      return tokenValid(body.token) ? json(200, { ok: true }) : json(401, { ok: false });
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
