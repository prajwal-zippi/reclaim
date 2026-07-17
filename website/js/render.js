/* ============================================================
   Reclaim Era — data-driven rendering
   Reads window.RE_DATA (js/site-data.js). If this browser has
   unpublished admin edits (saved by admin.html), those are
   previewed here instead — visitors never see them.
   ============================================================ */
(function () {
  "use strict";

  var PREVIEW_KEY = "re-site-data";

  var data = window.RE_DATA || {};
  var previewing = false;
  try {
    var draft = JSON.parse(localStorage.getItem(PREVIEW_KEY));
    if (draft && typeof draft === "object") {
      data = draft;
      previewing = true;
    }
  } catch (e) {}

  /* ---------- product artwork ---------- */
  var ART = {
    tote: '<svg viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/><circle cx="100" cy="104" r="86" fill="none" stroke="#00BF63" stroke-width="1.6" stroke-dasharray="5 7" opacity=".5"/><path d="M70 62 Q100 30 130 62" fill="none" stroke="#96543F" stroke-width="7" stroke-linecap="round"/><rect x="48" y="62" width="104" height="96" rx="12" fill="#3D5A99"/><rect x="48" y="62" width="104" height="30" rx="12" fill="#5C7BBD"/><rect x="56" y="70" width="88" height="80" rx="8" fill="none" stroke="#fff" stroke-width="1.6" stroke-dasharray="4 5" opacity=".55"/><rect x="76" y="108" width="48" height="30" rx="5" fill="#5C7BBD"/><circle cx="100" cy="123" r="6" fill="#00BF63"/></svg>',
    backpack: '<svg viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/><circle cx="100" cy="104" r="86" fill="none" stroke="#0522C8" stroke-width="1.6" stroke-dasharray="5 7" opacity=".35"/><path d="M78 56 Q100 38 122 56" fill="none" stroke="#96543F" stroke-width="7" stroke-linecap="round"/><rect x="52" y="56" width="96" height="104" rx="26" fill="#5E4034"/><rect x="52" y="56" width="96" height="104" rx="26" fill="none" stroke="#F4E7E1" stroke-width="1.6" stroke-dasharray="4 5" opacity=".5"/><rect x="66" y="112" width="68" height="48" rx="14" fill="#96543F"/><rect x="90" y="128" width="20" height="10" rx="4" fill="#E8B84B"/><path d="M66 88 h68" stroke="#F4E7E1" stroke-width="2" stroke-dasharray="4 5" opacity=".6"/><circle cx="100" cy="74" r="5" fill="#00BF63"/></svg>',
    organizer: '<svg viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/><circle cx="100" cy="104" r="86" fill="none" stroke="#96543F" stroke-width="1.6" stroke-dasharray="5 7" opacity=".4"/><rect x="46" y="58" width="108" height="92" rx="10" fill="#2E4B8F"/><rect x="46" y="58" width="108" height="92" rx="10" fill="none" stroke="#fff" stroke-width="1.6" stroke-dasharray="4 5" opacity=".5"/><rect x="120" y="58" width="34" height="92" rx="10" fill="#3D5A99"/><rect x="132" y="86" width="10" height="36" rx="5" fill="#96543F"/><rect x="58" y="74" width="44" height="6" rx="3" fill="#E8EBFB" opacity=".85"/><rect x="58" y="88" width="32" height="6" rx="3" fill="#E8EBFB" opacity=".55"/><circle cx="64" cy="136" r="6" fill="#00BF63"/></svg>',
    bundle: '<svg viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/><circle cx="100" cy="104" r="86" fill="none" stroke="#E8B84B" stroke-width="1.6" stroke-dasharray="5 7" opacity=".55"/><rect x="50" y="86" width="100" height="72" rx="10" fill="#0D3B28"/><rect x="50" y="86" width="100" height="20" rx="10" fill="#14532F"/><rect x="93" y="86" width="14" height="72" fill="#E8B84B"/><path d="M100 86 C 80 78 76 58 92 56 C 102 55 102 72 100 86 C 98 72 98 55 108 56 C 124 58 120 78 100 86Z" fill="#96543F"/><circle cx="100" cy="86" r="6" fill="#00BF63"/><rect x="50" y="86" width="100" height="72" rx="10" fill="none" stroke="#fff" stroke-width="1.4" stroke-dasharray="4 5" opacity=".35"/></svg>'
  };

  var HEART =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M19.5 12.6 12 20l-7.5-7.4a5 5 0 1 1 7.5-6.6 5 5 0 1 1 7.5 6.6Z"/></svg>';

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function card(p, variant, revealClass) {
    var art = ART[p.art] || ART.tote;
    var reveal = revealClass ? " " + revealClass : "";
    var inner =
      '<div class="prod-art">' + art + "</div>" +
      '<div class="prod-info">' +
      "<h4>" + esc(p.name) + "</h4>" +
      (p.price ? '<p class="prod-price">' + esc(p.price) + "</p>" : "") +
      (p.impact ? '<p class="imp">' + HEART + " " + esc(p.impact) + "</p>" : "");

    if (variant === "teaser") {
      return '<a href="shop.html" class="prod-card' + reveal + '">' + inner + "</div></a>";
    }
    return (
      '<div class="prod-card' + reveal + '">' + inner +
      (p.desc ? '<p style="font-size:.84rem;color:var(--ink-soft);margin-top:8px">' + esc(p.desc) + "</p>" : "") +
      '<a class="btn btn-ink btn-sm" style="margin-top:16px" href="contact.html">Order Inquiry</a>' +
      "</div></div>"
    );
  }

  function renderInto(el, d, opts) {
    opts = opts || {};
    var items = (d.products || []).filter(function (p) { return p.visible !== false; });
    if (opts.limit) items = items.slice(0, opts.limit);
    if (!items.length) {
      el.innerHTML =
        '<p style="grid-column:1/-1;color:var(--ink-soft)">New products are on their way. ' +
        'Write to <a href="mailto:reclaimera@gmail.com" style="text-decoration:underline">reclaimera@gmail.com</a> for current stock.</p>';
      return;
    }
    var delays = ["", "reveal-d1", "reveal-d2", "reveal-d3"];
    el.innerHTML = items
      .map(function (p, i) {
        var rc = opts.reveal ? ("reveal " + delays[i % 4]).trim() : "";
        return card(p, opts.variant || "full", rc);
      })
      .join("");
  }

  /* ---------- apply to page ---------- */
  document.querySelectorAll('[data-render="products"]').forEach(function (el) {
    renderInto(el, data, {
      variant: el.getAttribute("data-variant") || "full",
      limit: parseInt(el.getAttribute("data-limit") || "0", 10),
      reveal: true
    });
  });

  document.querySelectorAll("[data-stat]").forEach(function (el) {
    var v = (data.stats || {})[el.getAttribute("data-stat")];
    if (v) el.textContent = v;
  });

  if (data.phone) {
    document.querySelectorAll("[data-phone]").forEach(function (el) {
      el.textContent = data.phone;
      if (el.tagName === "A") el.href = "tel:" + String(data.phone).replace(/[^+\d]/g, "");
    });
  }

  /* small banner so the admin knows they are looking at a draft */
  if (previewing && !document.querySelector(".admin-preview-note")) {
    var note = document.createElement("div");
    note.className = "admin-preview-note";
    note.innerHTML =
      'Draft preview (only visible on this device) &nbsp;·&nbsp; <a href="admin.html" style="text-decoration:underline">Open dashboard</a>';
    note.style.cssText =
      "position:fixed;bottom:0;left:0;right:0;z-index:200;background:#E8B84B;color:#17251E;" +
      "font:600 13px/1.4 Inter,sans-serif;text-align:center;padding:8px 14px;";
    document.body.appendChild(note);
  }

  /* expose for admin.html */
  window.RE_RENDER = { ART: ART, card: card, renderInto: renderInto, esc: esc, PREVIEW_KEY: PREVIEW_KEY };
  window.__RE_ACTIVE_DATA = data;
})();
