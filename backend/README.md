# Reclaim Era — Campaign Application Backend

Flask + **Neon (serverless Postgres)** + Razorpay backend for the **Donation Campaign
Application** form (`campaign-application.html` on the website). Handles the mandatory
₹500 logistics fee: creates Razorpay orders, verifies payment signatures
cryptographically, and stores verified applications in a `campaign_applications` table
(created automatically on first start).

## Payment model (updated)

**Primary: direct UPI.** The form shows a QR + UPI intent link for the Trust's UPI ID
(`lampeducational@ybl`), the applicant pays Rs.500 in their UPI app and submits the
UTR reference. `POST /api/campaign/submit-upi` stores the application with status
`upi_claimed`. **The team must verify the Rs.500 against the bank/UPI statement**
(match the UTR) before confirming a campaign — a submitted UTR is a claim, not proof.
View pending ones in Neon:
`SELECT app_ref, institution_name, contact_phone, upi_utr, created_at FROM campaign_applications WHERE status = 'upi_claimed';`

**Optional: Razorpay.** The gateway endpoints still exist but stay dormant until real
`RAZORPAY_KEY_ID/SECRET` values are set (they return 503 otherwise).

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/campaign/submit-upi` | Direct-UPI flow: validates the form + UTR, stores the application as `upi_claimed` for manual verification |
| POST | `/api/campaign/create-order` | Validates the form data, creates a ₹500 Razorpay order, stores the application as `payment_pending`, returns `order_id` + public `key_id` |
| POST | `/api/campaign/verify-payment` | Verifies `razorpay_order_id` / `razorpay_payment_id` / `razorpay_signature` with Razorpay's crypto util, marks the application `paid` |
| GET | `/api/health` | Liveness check |

The ₹500 amount is defined **server-side only** (`LOGISTICS_FEE_PAISE`) — the client
can never change what is charged. The key secret never leaves the server.

## Setup

### 1. Razorpay keys
1. Sign in at https://dashboard.razorpay.com (the Trust's account — NGOs need KYC
   with 12A/80G documents before **live** keys are issued).
2. Account & Settings → API Keys → Generate **Test** keys first.
3. Test mode accepts UPI (`success@razorpay`), test cards, and netbanking without
   real money. UPI/Cards/NetBanking are enabled by default in Standard Checkout.

### 2. Neon database
1. Sign up free at https://neon.tech (the client's account) and create a project.
2. On the project dashboard press **Connect** and copy the connection string —
   it looks like `postgresql://user:pass@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require`.
3. That string is your `DATABASE_URL`. The app creates the
   `campaign_applications` table automatically on first start; view submissions
   any time in Neon's **Tables** tab or with
   `SELECT * FROM campaign_applications ORDER BY created_at DESC;` in the SQL editor.

### 3. Environment variables
```bash
cd backend
cp .env.example .env
# edit .env and fill in:
#   RAZORPAY_KEY_ID / RAZORPAY_KEY_SECRET
#   DATABASE_URL (Neon)
#   ALLOWED_ORIGIN (your site URL in production)
```
The app refuses to start if the Razorpay variables are missing — credentials are
never hardcoded.

### 4. Run locally
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py            # serves on http://localhost:5001
```
Then open the website's `campaign-application.html` (the page's `API_BASE` defaults
to `http://localhost:5001` when browsing on localhost) and submit a test
application with a test UPI/card.

### 5. Deploy
Any Python host works (Render / Railway / Fly.io free tiers are fine):
- Start command: `gunicorn app:app`
- Set the four environment variables in the host's dashboard.
- Set `ALLOWED_ORIGIN` to the website's exact origin, e.g. `https://reclaimera.in`.
- Finally, edit `campaign-application.html` and set `CAMPAIGN_API_BASE` to the
  deployed URL (marked with a `CHANGE ME` comment).

## Go-live checklist
- [ ] Razorpay KYC approved → switch `.env` to `rzp_live_...` keys
- [ ] `ALLOWED_ORIGIN` set to the production domain
- [ ] `CAMPAIGN_API_BASE` on the page pointed at the deployed backend
- [ ] One real ₹500 end-to-end test, then refund it from the Razorpay dashboard
- [ ] (Recommended, later) add a Razorpay **webhook** for `payment.captured` as a
      belt-and-braces record in case a user closes the tab before verification
