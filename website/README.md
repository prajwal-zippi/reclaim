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
| Host a Campaign (multi-step + PayU ₹500 minimum link) | `campaign-application.html` |

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

## Campaign application (PayU Payment Link)

`campaign-application.html` is a 3-step form (location → contact → review). On the
final step, pressing **Continue to secure payment** sends the application details to
`reclaimera@gmail.com` (via FormSubmit) and opens the client's **PayU Payment Link**
in a new tab. The minimum contribution is ₹500. Fully static — no backend or database
is required for this flow.

The client-approved links are configured in `_dev/build.py` near the top as
`DONATE_FORM_LINK` (Jotform) and `PAYMENT_LINK` (PayU). Run
`python3 _dev/build.py` after changing either value.

The `Request a Pick-Up` button stays as a scheduling form. Pickup is charged at
transport cost; the current prices and distance rules are shown on that page.

## Admin dashboard

`admin.html` lets the client manage shop products, gallery entries, impact numbers and
the contact phone number. `admin-content.html` manages the seller profile, team,
contributors, volunteers, environmental education resources, and map branches.

- Login is always server-verified against a PBKDF2 password hash stored in Neon. There
  is no client-side fallback password.
- Set `DATABASE_URL`, `ADMIN_SESSION_SECRET`, `ADMIN_INITIAL_PASSWORD`, and optionally
  `ADMIN_INITIAL_USERNAME` in Netlify before the first login.
- Passwords require at least eight characters with uppercase, lowercase, a number and
  a special symbol. The dashboard can change both username and password.
- Changes publish to Neon automatically and are reflected on public pages immediately.
  The download button creates a complete local backup; it is not required to publish.

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
