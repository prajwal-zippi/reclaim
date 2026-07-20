/* ============================================================
   Site configuration.

   RE_HAS_BACKEND:
     false = pure static site (no /api). The shop/gallery render from the
             static files (js/site-data.js + js/gallery-data.js); the admin
             dashboard edits and publishes via "Download to publish".
     true  = a backend is deployed (Neon live-save + image uploads). Also set
             RE_API_BASE to the backend URL, or "" if it is on the same domain.
   ============================================================ */
window.RE_HAS_BACKEND = false;
window.RE_API_BASE = "";
