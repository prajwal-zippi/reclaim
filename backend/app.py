"""
Reclaim Era — Campaign Application backend
LAMP Educational and Charitable Trust

Flask + Neon (serverless Postgres) + Razorpay.

Endpoints
  POST /api/campaign/create-order    validate form data, create a Razorpay
                                     order for the Rs.500 logistics fee, store
                                     the application as payment_pending
  POST /api/campaign/verify-payment  verify the Razorpay signature, mark the
                                     application paid
  GET  /api/health                   liveness probe

Credentials are read from environment variables only — see .env.example.
"""

import hashlib
import hmac as hmac_mod
import os
import re
import secrets
import time
from datetime import datetime, timezone

import psycopg
import razorpay
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv()

# ---------------------------------------------------------------- config
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")
DATABASE_URL = os.environ.get("DATABASE_URL")  # Neon connection string (postgresql://...sslmode=require)
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be set (your Neon connection string).")

# Razorpay is OPTIONAL now that direct UPI is the primary payment path.
# If keys are configured (never hardcoded), the gateway endpoints activate.
RAZORPAY_ENABLED = bool(
    RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET and "REPLACE" not in RAZORPAY_KEY_ID
)

LOGISTICS_FEE_PAISE = 50000  # Rs.500 — authoritative amount lives here, never trusted from the client
CURRENCY = "INR"

# ---- admin auth ----
# Signing key for session tokens. Set SECRET_KEY in production for stability
# across DATABASE_URL rotations; falls back to a derivation of the DB URL.
SECRET_KEY = os.environ.get("SECRET_KEY") or hashlib.sha256(
    ("re-admin::" + DATABASE_URL).encode()
).hexdigest()
TOKEN_TTL_SECONDS = 12 * 3600
DEFAULT_ADMIN_PASSWORD = "Reclaim@2026"  # seeded once; must be changed after first login
PBKDF2_ITERATIONS = 240_000


def hash_password(pw: str) -> str:
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), bytes.fromhex(salt), PBKDF2_ITERATIONS)
    return f"pbkdf2${salt}${dk.hex()}"


def verify_password(pw: str, stored: str) -> bool:
    try:
        _, salt, digest = stored.split("$")
        dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), bytes.fromhex(salt), PBKDF2_ITERATIONS)
        return hmac_mod.compare_digest(dk.hex(), digest)
    except Exception:
        return False


def make_token() -> str:
    exp = str(int(time.time()) + TOKEN_TTL_SECONDS)
    sig = hmac_mod.new(SECRET_KEY.encode(), exp.encode(), hashlib.sha256).hexdigest()
    return exp + "." + sig


def token_valid(tok: str) -> bool:
    try:
        exp, sig = tok.split(".")
        good = hmac_mod.new(SECRET_KEY.encode(), exp.encode(), hashlib.sha256).hexdigest()
        return hmac_mod.compare_digest(sig, good) and int(exp) > time.time()
    except Exception:
        return False


def password_meets_policy(pw: str) -> bool:
    return bool(
        len(pw) >= 8
        and re.search(r"[A-Z]", pw)
        and re.search(r"[a-z]", pw)
        and re.search(r"\d", pw)
        and re.search(r"[^A-Za-z0-9]", pw)
    )
LOCATION_TYPES = [
    "Apartment Complex", "Companies", "School", "College/University",
    "Small/Medium Business (SMB)", "Restaurants/GYM/Hotels/Super Markets/Malls", "Other",
]

app = Flask(__name__)
CORS(app, origins=[ALLOWED_ORIGIN] if ALLOWED_ORIGIN != "*" else "*")

rzp = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)) if RAZORPAY_ENABLED else None


def db():
    return psycopg.connect(DATABASE_URL)


SCHEMA = """
CREATE TABLE IF NOT EXISTS campaign_applications (
  id                  SERIAL PRIMARY KEY,
  location_type       TEXT NOT NULL,
  location_other      TEXT,
  institution_name    TEXT NOT NULL,
  address             TEXT NOT NULL,
  contact_name        TEXT NOT NULL,
  contact_phone       TEXT NOT NULL,
  contact_email       TEXT NOT NULL,
  status              TEXT NOT NULL DEFAULT 'payment_pending',
  razorpay_order_id   TEXT UNIQUE NOT NULL,
  razorpay_payment_id TEXT,
  razorpay_signature  TEXT,
  payment_method      TEXT,
  payment_status      TEXT,
  amount_paise        INTEGER NOT NULL,
  currency            TEXT NOT NULL,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  paid_at             TIMESTAMPTZ,
  failed_at           TIMESTAMPTZ
);
"""

ADMIN_SCHEMA = """
CREATE TABLE IF NOT EXISTS admin_settings (
  id            SMALLINT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  password_hash TEXT NOT NULL,
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

MIGRATIONS = [
    "ALTER TABLE campaign_applications ALTER COLUMN razorpay_order_id DROP NOT NULL",
    "ALTER TABLE campaign_applications ADD COLUMN IF NOT EXISTS upi_utr TEXT",
    "ALTER TABLE campaign_applications ADD COLUMN IF NOT EXISTS app_ref TEXT UNIQUE",
]

try:
    with db() as conn:
        conn.execute(SCHEMA)
        conn.execute(ADMIN_SCHEMA)
        for mig in MIGRATIONS:
            try:
                conn.execute(mig)
            except Exception:
                pass
        # seed the default admin password once (change it after first login;
        # to reset a forgotten password: DELETE FROM admin_settings; then restart)
        conn.execute(
            "INSERT INTO admin_settings (id, password_hash) VALUES (1, %s) ON CONFLICT (id) DO NOTHING",
            (hash_password(DEFAULT_ADMIN_PASSWORD),),
        )
except Exception as exc:  # don't block boot on a cold DB; requests will surface errors
    print(f"WARNING: could not initialise database schema at startup: {exc}")

PHONE_RE = re.compile(r"^(\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ---------------------------------------------------------------- helpers
def validate_application(data):
    """Server-side validation mirroring the frontend. Returns an errors dict."""
    errors = {}

    if data.get("location_type") not in LOCATION_TYPES:
        errors["location_type"] = "Choose the type of location."
    elif data.get("location_type") == "Other" and len((data.get("location_other") or "").strip()) < 2:
        errors["location_other"] = "Tell us what kind of location this is."

    if len((data.get("institution_name") or "").strip()) < 2:
        errors["institution_name"] = "Enter the name of the institution or apartment complex."

    if len((data.get("address") or "").strip()) < 10:
        errors["address"] = "Enter the complete address, including area and PIN code."

    if len((data.get("contact_name") or "").strip()) < 2:
        errors["contact_name"] = "Enter the coordinator or contact person's name."

    if not PHONE_RE.match((data.get("contact_phone") or "").strip()):
        errors["contact_phone"] = "Enter a valid Indian mobile number."

    if not EMAIL_RE.match((data.get("contact_email") or "").strip()):
        errors["contact_email"] = "Enter a valid email address."

    return errors


def clean(data):
    return {
        "location_type": data.get("location_type"),
        "location_other": (data.get("location_other") or "").strip() or None,
        "institution_name": (data.get("institution_name") or "").strip(),
        "address": (data.get("address") or "").strip(),
        "contact_name": (data.get("contact_name") or "").strip(),
        "contact_phone": (data.get("contact_phone") or "").strip(),
        "contact_email": (data.get("contact_email") or "").strip().lower(),
    }


# ---------------------------------------------------------------- routes
@app.get("/api/health")
def health():
    return jsonify({"ok": True, "razorpay_enabled": RAZORPAY_ENABLED})


@app.post("/api/admin/login")
def admin_login():
    password = (request.get_json(silent=True) or {}).get("password") or ""
    time.sleep(0.4)  # slow down brute-force attempts
    with db() as conn:
        row = conn.execute("SELECT password_hash FROM admin_settings WHERE id = 1").fetchone()
    if not row or not verify_password(password, row[0]):
        return jsonify({"ok": False, "error": "Wrong password."}), 401
    return jsonify({"ok": True, "token": make_token()})


@app.post("/api/admin/check")
def admin_check():
    tok = (request.get_json(silent=True) or {}).get("token") or ""
    if token_valid(tok):
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 401


@app.post("/api/admin/change-password")
def admin_change_password():
    data = request.get_json(silent=True) or {}
    if not token_valid(data.get("token") or ""):
        return jsonify({"ok": False, "error": "Session expired. Log in again."}), 401

    current = data.get("current_password") or ""
    new = data.get("new_password") or ""

    if not password_meets_policy(new):
        return jsonify({
            "ok": False,
            "error": "New password must be at least 8 characters and include an uppercase letter, a lowercase letter, a number and a special symbol.",
        }), 400

    with db() as conn:
        row = conn.execute("SELECT password_hash FROM admin_settings WHERE id = 1").fetchone()
        if not row or not verify_password(current, row[0]):
            return jsonify({"ok": False, "error": "Current password is wrong."}), 401
        conn.execute(
            "UPDATE admin_settings SET password_hash = %s, updated_at = now() WHERE id = 1",
            (hash_password(new),),
        )
    return jsonify({"ok": True})


UTR_RE = re.compile(r"^[A-Za-z0-9]{10,23}$")


@app.post("/api/campaign/submit-upi")
def submit_upi():
    """Direct-UPI flow: the applicant has paid Rs.500 to the Trust's UPI ID and
    submits the UTR reference. Stored as upi_claimed for manual verification
    against the bank statement before the campaign is confirmed."""
    data = request.get_json(silent=True) or {}

    errors = validate_application(data)
    utr = (data.get("upi_utr") or "").strip()
    if not UTR_RE.match(utr):
        errors["upi_utr"] = "Enter the UPI reference / UTR number shown in your payment app."

    # minimum Rs.500; paying more is welcome (sanity cap to catch typos)
    try:
        amount_rupees = int(data.get("amount_paid") or 0)
    except (TypeError, ValueError):
        amount_rupees = 0
    if not (500 <= amount_rupees <= 100000):
        errors["amount_paid"] = "The minimum logistics fee is Rs.500."

    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    form = clean(data)
    app_ref = "RE-" + secrets.token_hex(4).upper()

    with db() as conn:
        conn.execute(
            """
            INSERT INTO campaign_applications
              (location_type, location_other, institution_name, address, contact_name,
               contact_phone, contact_email, amount_paise, currency,
               status, payment_method, upi_utr, app_ref)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'upi_claimed', 'upi-direct', %s, %s)
            """,
            (
                form["location_type"], form["location_other"], form["institution_name"],
                form["address"], form["contact_name"], form["contact_phone"],
                form["contact_email"], amount_rupees * 100, CURRENCY, utr, app_ref,
            ),
        )

    return jsonify({"ok": True, "application_id": app_ref})


@app.post("/api/campaign/create-order")
def create_order():
    if rzp is None:
        return jsonify({"ok": False, "error": "Card/netbanking payments are not enabled yet. Please pay by UPI."}), 503
    data = request.get_json(silent=True) or {}

    errors = validate_application(data)
    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    form = clean(data)

    order = rzp.order.create(
        {
            "amount": LOGISTICS_FEE_PAISE,
            "currency": CURRENCY,
            "receipt": f"campaign-{int(datetime.now(timezone.utc).timestamp())}",
            "notes": {
                "purpose": "Reclaim Era campaign logistics fee",
                "institution": form["institution_name"][:100],
            },
        }
    )

    with db() as conn:
        conn.execute(
            """
            INSERT INTO campaign_applications
              (location_type, location_other, institution_name, address, contact_name,
               contact_phone, contact_email, razorpay_order_id, amount_paise, currency)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                form["location_type"], form["location_other"], form["institution_name"],
                form["address"], form["contact_name"], form["contact_phone"],
                form["contact_email"], order["id"], LOGISTICS_FEE_PAISE, CURRENCY,
            ),
        )

    return jsonify(
        {
            "ok": True,
            "order_id": order["id"],
            "amount": LOGISTICS_FEE_PAISE,
            "currency": CURRENCY,
            "key_id": RAZORPAY_KEY_ID,  # public key only — the secret never leaves the server
        }
    )


@app.post("/api/campaign/verify-payment")
def verify_payment():
    if rzp is None:
        return jsonify({"ok": False, "error": "Gateway payments are not enabled."}), 503
    data = request.get_json(silent=True) or {}
    order_id = data.get("razorpay_order_id")
    payment_id = data.get("razorpay_payment_id")
    signature = data.get("razorpay_signature")

    if not (order_id and payment_id and signature):
        return jsonify({"ok": False, "error": "Missing payment fields."}), 400

    try:
        rzp.utility.verify_payment_signature(
            {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
        )
    except razorpay.errors.SignatureVerificationError:
        with db() as conn:
            conn.execute(
                "UPDATE campaign_applications SET status = 'signature_failed', failed_at = now() "
                "WHERE razorpay_order_id = %s",
                (order_id,),
            )
        return jsonify({"ok": False, "error": "Payment verification failed."}), 400

    # signature is authentic — enrich with payment details (best effort)
    method = pay_status = None
    try:
        p = rzp.payment.fetch(payment_id)
        method, pay_status = p.get("method"), p.get("status")
    except Exception:
        pass

    with db() as conn:
        cur = conn.execute(
            """
            UPDATE campaign_applications
               SET status = 'paid',
                   razorpay_payment_id = %s,
                   razorpay_signature = %s,
                   payment_method = COALESCE(%s, payment_method),
                   payment_status = COALESCE(%s, payment_status),
                   paid_at = now()
             WHERE razorpay_order_id = %s
            """,
            (payment_id, signature, method, pay_status, order_id),
        )
        if cur.rowcount == 0:
            return jsonify({"ok": False, "error": "Application not found for this order."}), 404

    return jsonify({"ok": True, "application_id": order_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)), debug=False)
