# Reclaim Era — Website

Static website for **Reclaim Era** (Lamp Educational and Charitable Trust), built from the
sitemap and content brief in `Reclaim Era_Sitemap Overview.pdf`.

> Waste to Wisdom — Revive. Recycle. Rise.

## Pages (13)

| Page | File |
|---|---|
| Home | `index.html` |
| About Us | `about.html` |
| Our Initiatives (landing) | `initiatives.html` |
| — Waste Management | `waste-management.html` |
| — Education (NEP 2020) | `education.html` |
| — EmpowHer Academy | `empowher.html` |
| — CSR Partnerships | `csr-partnerships.html` |
| Shop With Purpose | `shop.html` |
| Request a Pick-Up | `request-pickup.html` |
| Zero Waste Certification & AMC | `zero-waste-certification.html` |
| Get Involved | `get-involved.html` |
| Resources & FAQs | `resources.html` |
| Contact | `contact.html` |
| Host a Campaign (multi-step + Razorpay ₹500 link) | `campaign-application.html` |

## Structure

```
website/
├── *.html            ← the pages
├── css/style.css     ← all styling (brand palette, layout, responsive)
├── js/main.js        ← menu, animations, counters, accordions, forms
├── assets/           ← favicon (round "re." mark) + original logo PNG
└── _dev/build.py     ← page generator (see Editing below)
```

The header and footer use the horizontal **"reclaim era."** wordmark, recreated in
HTML/CSS so it stays crisp at any size. The round "re." logo is used as the favicon.

## Editing

Pages are plain HTML — edit them directly. Because all 13 pages share the same header
and footer, there's also a generator at `_dev/build.py` that rebuilds every page from one
template (`python3 _dev/build.py`). Use it for site-wide changes (nav, footer), or ignore
it entirely and edit the HTML by hand.

## Preview locally

```bash
cd website
python3 -m http.server 8000
# open http://localhost:8000
```

(Opening `index.html` directly in a browser also works.)

## Deploying

The site is plain HTML/CSS/JS — host it anywhere: Netlify / Vercel / GitHub Pages /
any shared hosting. Just upload the contents of this folder.

## Campaign application (Razorpay Payment Link)

`campaign-application.html` is a 3-step form (location → contact → review). On the
final step, pressing **Pay ₹500 via Razorpay** sends the application details to
`reclaimera@gmail.com` (via FormSubmit) and opens the client's **Razorpay Payment
Link** in a new tab to collect the fee. Fully static — no backend, no database.

**Paste the real links** in `_dev/build.py` near the top:
`RZP_DONATE` (a Razorpay Payment Link that lets donors enter any amount) and
`RZP_CAMPAIGN` (a link for the ₹500 minimum fee), then run `python3 _dev/build.py`.
Until they're set, Donate buttons show a friendly "payments open shortly" toast and
the campaign form still captures the application by email. Razorpay Payment Links
require the Trust's Razorpay account (KYC) to create and to receive money.

The `Request a Pick-Up` button is deliberately **not** a payment link — pickups are
free, so it stays as the scheduling form.

## Admin dashboard

`admin.html` (not linked from the site — share the URL privately) lets the client edit
**shop products** (add/remove/reorder/hide, names, prices, impact lines, artwork),
the **impact numbers** in the home hero, and the **contact phone number**.

- **Login**: if the optional backend (`../backend/`) is running, login is server-verified
  against a PBKDF2 hash in Neon and the password can be changed from the dashboard. On
  pure-static hosting (no backend) it falls back to a client-side passcode in `admin.html`
  (`FALLBACK_PASSCODE`, convenience-only — keep the /admin.html URL private). Default in
  both cases: `Reclaim@2026` — **change it right after the
  first login** using the "Admin password" section (minimum 8 characters with an
  uppercase letter, a lowercase letter, a number and a special symbol — enforced by
  the server). Forgot it? Run `DELETE FROM admin_settings;` in Neon's SQL editor and
  restart the backend — it re-seeds the default.
- Edits save instantly as a draft **on that device only** and can be previewed across the
  site (a yellow "draft preview" bar appears).
- **Publish** = press "Download publish file" and replace `js/site-data.js` on the
  hosting with the downloaded file. That's the only step that changes the live site.
- The shop grids, hero impact chips, and phone placeholders all render from
  `js/site-data.js` via `js/render.js`.

## Before going live — placeholders to replace

- **Social links**: Instagram is live (instagram.com/reclaimera.official); the footer
  Facebook/LinkedIn icons still point to `#` until those URLs exist.
- **Forms are LIVE** via FormSubmit.co (free, unlimited submissions): the pickup,
  contact, and newsletter forms POST to `https://formsubmit.co/reclaimera@gmail.com`
  (AJAX via the `/ajax/` endpoint, with a plain-POST fallback when JavaScript is off).
  Each form sets its own `_subject`, uses FormSubmit's `_honey` honeypot, `_captcha`
  is disabled, and emails arrive in table format. **One-time step: the first submission
  sends an activation email to reclaimera@gmail.com — the client must click Activate
  before enquiries are delivered.** Optional hardening: after activation, FormSubmit
  provides a random alias endpoint that hides the email address; swap it into the three
  form `action` attributes if desired. Submissions arrive as email only (no dashboard),
  so tell the client not to delete enquiry emails.
- **Resources page**: blog / report / case-study / media-kit cards link to `#` until the
  documents exist.
- **Shop**: product cards route to the contact page for order inquiries; swap in a real
  e-commerce flow when ready.
- **Kannada toggle** (`EN · ಕನ್ನಡ` in the top bar) is visual only — bilingual content is a
  future phase per the brief.

## Brand tokens (from the logo)

| Token | Value |
|---|---|
| Blue ("r") | `#0522C8` |
| Terracotta ("e") | `#96543F` |
| Green (dot) | `#00BF63` |
| Ink | `#17251E` |
| Cream background | `#FAF6EE` |

Fonts: [Poppins](https://fonts.google.com/specimen/Poppins) (headings, matches the
wordmark) + [Inter](https://fonts.google.com/specimen/Inter) (body), loaded from Google Fonts.

The site is mobile-first: the menu collapses to a full-screen panel, primary actions sit
in a sticky bottom bar, and all forms and cards are single-column on phones.
