/* ============================================================
   Reclaim Era — data-driven rendering
   Precedence for what the site shows:
     1. LIVE content from the backend/Neon (/api/content)
     2. the static files js/site-data.js + js/gallery-data.js (fallback)
   The static files paint instantly; live content re-renders when it
   arrives, so visitors never wait on a cold backend.
   ============================================================ */
(function () {
  "use strict";

  var PREVIEW_KEY = "re-site-data";
  var API_BASE =
    (location.hostname === "localhost" || location.hostname === "127.0.0.1")
      ? "http://localhost:5001"
      : (window.RE_API_BASE || "");

  /* ---------- product artwork ---------- */
  var ART = {
    tote: '<svg viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/><circle cx="100" cy="104" r="86" fill="none" stroke="#00BF63" stroke-width="1.6" stroke-dasharray="5 7" opacity=".5"/><path d="M70 62 Q100 30 130 62" fill="none" stroke="#96543F" stroke-width="7" stroke-linecap="round"/><rect x="48" y="62" width="104" height="96" rx="12" fill="#3D5A99"/><rect x="48" y="62" width="104" height="30" rx="12" fill="#5C7BBD"/><rect x="56" y="70" width="88" height="80" rx="8" fill="none" stroke="#fff" stroke-width="1.6" stroke-dasharray="4 5" opacity=".55"/><rect x="76" y="108" width="48" height="30" rx="5" fill="#5C7BBD"/><circle cx="100" cy="123" r="6" fill="#00BF63"/></svg>',
    backpack: '<svg viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/><circle cx="100" cy="104" r="86" fill="none" stroke="#0522C8" stroke-width="1.6" stroke-dasharray="5 7" opacity=".35"/><path d="M78 56 Q100 38 122 56" fill="none" stroke="#96543F" stroke-width="7" stroke-linecap="round"/><rect x="52" y="56" width="96" height="104" rx="26" fill="#5E4034"/><rect x="52" y="56" width="96" height="104" rx="26" fill="none" stroke="#F4E7E1" stroke-width="1.6" stroke-dasharray="4 5" opacity=".5"/><rect x="66" y="112" width="68" height="48" rx="14" fill="#96543F"/><rect x="90" y="128" width="20" height="10" rx="4" fill="#E8B84B"/><path d="M66 88 h68" stroke="#F4E7E1" stroke-width="2" stroke-dasharray="4 5" opacity=".6"/><circle cx="100" cy="74" r="5" fill="#00BF63"/></svg>',
    organizer: '<svg viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/><circle cx="100" cy="104" r="86" fill="none" stroke="#96543F" stroke-width="1.6" stroke-dasharray="5 7" opacity=".4"/><rect x="46" y="58" width="108" height="92" rx="10" fill="#2E4B8F"/><rect x="46" y="58" width="108" height="92" rx="10" fill="none" stroke="#fff" stroke-width="1.6" stroke-dasharray="4 5" opacity=".5"/><rect x="120" y="58" width="34" height="92" rx="10" fill="#3D5A99"/><rect x="132" y="86" width="10" height="36" rx="5" fill="#96543F"/><rect x="58" y="74" width="44" height="6" rx="3" fill="#E8EBFB" opacity=".85"/><rect x="58" y="88" width="32" height="6" rx="3" fill="#E8EBFB" opacity=".55"/><circle cx="64" cy="136" r="6" fill="#00BF63"/></svg>',
    bundle: '<svg viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/><circle cx="100" cy="104" r="86" fill="none" stroke="#E8B84B" stroke-width="1.6" stroke-dasharray="5 7" opacity=".55"/><rect x="50" y="86" width="100" height="72" rx="10" fill="#0D3B28"/><rect x="50" y="86" width="100" height="20" rx="10" fill="#14532F"/><rect x="93" y="86" width="14" height="72" fill="#E8B84B"/><path d="M100 86 C 80 78 76 58 92 56 C 102 55 102 72 100 86 C 98 72 98 55 108 56 C 124 58 120 78 100 86Z" fill="#96543F"/><circle cx="100" cy="86" r="6" fill="#00BF63"/><rect x="50" y="86" width="100" height="72" rx="10" fill="none" stroke="#fff" stroke-width="1.4" stroke-dasharray="4 5" opacity=".35"/></svg>'
  };
  var HEART =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M19.5 12.6 12 20l-7.5-7.4a5 5 0 1 1 7.5-6.6 5 5 0 1 1 7.5 6.6Z"/></svg>';
  var IMPACT_ICONS = {
    recycle: '<path d="m8 7 3-4 3 4M11 3v7M17 10l4 2-2 4M21 12l-6 3M9 19l-4-1 1-4M5 18l4-6"/>',
    livelihood: '<circle cx="12" cy="7" r="3"/><path d="M5 21c.5-5 3-8 7-8s6.5 3 7 8M18 4v4M16 6h4"/>',
    school: '<path d="m3 10 9-6 9 6-9 6Z"/><path d="M7 13v5c3 2 7 2 10 0v-5M21 10v6"/>',
    leaf: '<path d="M5 21c1-10 6-16 15-17 0 11-5 16-12 16"/><path d="M5 21c3-7 7-10 11-12"/>',
    people: '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="10" r="2.3"/><path d="M3 21c.4-5 2.5-8 6-8s5.6 3 6 8M15 15c3 0 5 2 5.5 6"/>',
    bag: '<path d="M6 8h12l2 13H4Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    bicycle: '<circle cx="6" cy="17" r="4"/><circle cx="18" cy="17" r="4"/><path d="m6 17 4-8 4 8h-8M10 9h4l4 8M9 6h3"/>',
    run: '<circle cx="15" cy="4" r="2"/><path d="m12 8 3 2 3 4M12 8l-3 5 4 2-3 6M13 15l4 6"/>',
    book: '<path d="M12 6c-2-1.5-4.5-2-8-2v14c3.5 0 6 .5 8 2 2-1.5 4.5-2 8-2V4c-3.5 0-6 .5-8 2Z"/><path d="M12 6v14"/>'
  };

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  /* uploaded images live at /api/image/... on the backend; prefix API_BASE so they
     resolve whether the backend is same-origin or on a separate host. https links pass through. */
  function resolveImg(u) { return (u && u.indexOf("/api/") === 0) ? API_BASE + u : u; }

  /* ---------- shop cards ---------- */
  function card(p, variant, revealClass) {
    var media = p.imageUrl
      ? '<img src="' + esc(resolveImg(p.imageUrl)) + '" alt="' + esc(p.name) + '" loading="lazy" decoding="async">'
      : (ART[p.art] || ART.tote);
    var reveal = revealClass ? " " + revealClass : "";
    var inner =
      '<div class="prod-art' + (p.imageUrl ? " has-img" : "") + '">' + media + "</div>" +
      '<div class="prod-info">' +
      "<h4>" + esc(p.name) + "</h4>" +
      (p.price ? '<p class="prod-price">' + esc(p.price) + "</p>" : "") +
      (p.impact ? '<p class="imp">' + HEART + " " + esc(p.impact) + "</p>" : "");
    if (variant === "teaser") {
      return '<a href="shop.html" class="prod-card' + reveal + '">' + inner + "</div></a>";
    }
    return (
      '<div class="prod-card' + reveal + '">' + inner +
      (p.desc ? '<p class="prod-desc">' + esc(p.desc) + "</p>" : "") +
      '<a class="btn btn-ink btn-sm prod-inquiry" href="contact.html">Enquire to order <span aria-hidden="true">↗</span></a>' +
      "</div></div>"
    );
  }
  function renderProducts(el, products, opts) {
    opts = opts || {};
    var items = (products || []).filter(function (p) { return p.visible !== false; });
    if (opts.limit) items = items.slice(0, opts.limit);
    if (!items.length) {
      el.innerHTML =
        '<p style="grid-column:1/-1;color:var(--ink-soft)">New products are on their way. ' +
        'Write to <a href="mailto:reclaimera@gmail.com" style="text-decoration:underline">reclaimera@gmail.com</a> for current stock.</p>';
      return;
    }
    var delays = ["", "reveal-d1", "reveal-d2", "reveal-d3"];
    el.innerHTML = items.map(function (p, i) {
      var rc = opts.reveal ? ("reveal " + delays[i % 4]).trim() : "";
      return card(p, opts.variant || "full", rc);
    }).join("");
    /* Products are rendered again when live Neon content arrives. Those new
       nodes were not present when main.js created its IntersectionObserver,
       so ensure they enter instead of remaining permanently opacity: 0. */
    if (opts.reveal) {
      window.requestAnimationFrame(function () {
        el.querySelectorAll(".reveal").forEach(function (cardEl) {
          cardEl.classList.add("in");
        });
      });
    }
  }

  /* ---------- gallery cards ---------- */
  function renderGallery(grid, events) {
    events = (events || []).filter(function (x) { return x && (x.title || x.imageUrl); });
    var empty = document.getElementById("galleryEmpty");
    if (!events.length) { grid.innerHTML = ""; if (empty) empty.style.display = "block"; return; }
    if (empty) empty.style.display = "none";
    grid.innerHTML = events.map(function (ev) {
      var src = resolveImg(ev.imageUrl);
      var media = ev.imageUrl
        ? '<img src="' + esc(src) + '" alt="' + esc(ev.title) + '" loading="lazy" decoding="async">'
        : '<div class="gal-ph"><span>Photo coming soon</span></div>';
      var date = ev.date ? '<span class="gal-date">' + esc(ev.date) + "</span>" : "";
      var attrs = ev.imageUrl
        ? ' has-img" role="button" tabindex="0" aria-label="Open image: ' + esc(ev.title)
          + '" data-full="' + esc(src) + '" data-title="' + esc(ev.title) + '"'
        : '"';
      return '<article class="gal-card' + attrs + '>'
        + '<div class="gal-media">' + media + date + "</div>"
        + '<div class="gal-body"><h3>' + esc(ev.title) + "</h3>"
        + (ev.description ? "<p>" + esc(ev.description) + "</p>" : "") + "</div></article>";
    }).join("");
  }

  function safeHttps(value) {
    try { return new URL(String(value || "")).protocol === "https:" ? String(value) : ""; }
    catch (e) { return ""; }
  }

  function initials(name) {
    return String(name || "").split(/\s+/).filter(Boolean).slice(0, 2).map(function (part) {
      return part.charAt(0).toUpperCase();
    }).join("") || "RE";
  }

  function renderTeam(data) {
    var root = document.querySelector('[data-render="team"]');
    if (!root) return;
    var team = data.team || {};
    var categories = [
      ["core", "Core Team"],
      ["contributors", "Contributors"],
      ["volunteers", "Volunteers"]
    ];
    root.innerHTML = categories.map(function (entry) {
      var members = Array.isArray(team[entry[0]]) ? team[entry[0]] : [];
      if (!members.length) return "";
      var cards = members.map(function (member) {
        var href = safeHttps(member.profileUrl);
        var photo = member.imageUrl
          ? '<img src="' + esc(resolveImg(member.imageUrl)) + '" alt="' + esc(member.name) + '" loading="lazy" decoding="async">'
          : '<span>' + esc(initials(member.name)) + "</span>";
        var body = '<div class="team-photo">' + photo + "</div><h4>" + esc(member.name) + "</h4>"
          + '<p class="role">' + esc(member.role) + "</p>"
          + (member.description ? "<p>" + esc(member.description) + "</p>" : "")
          + (href ? '<span class="profile-link">View profile ↗</span>' : "");
        return href
          ? '<a class="team-card team-card-link" href="' + esc(href) + '" target="_blank" rel="noopener noreferrer">' + body + "</a>"
          : '<article class="team-card">' + body + "</article>";
      }).join("");
      return '<section class="team-category"><div class="team-category-head"><p class="eyebrow">' + entry[1]
        + '</p><span>' + members.length + (members.length === 1 ? " member" : " members") + '</span></div><div class="team-grid">' + cards + "</div></section>";
    }).join("");
  }

  function renderSeller(data) {
    var root = document.querySelector('[data-render="seller"]');
    if (!root) return;
    var sellers = Array.isArray(data.sellers) ? data.sellers.slice() : [];
    if (!sellers.length && data.seller) sellers = [{id:"legacy-seller",name:data.seller.name,biography:data.seller.description,websiteUrl:data.seller.profileUrl,visible:true,order:0}];
    sellers = sellers.filter(function(s){return s && s.visible !== false;}).sort(function(a,b){return Number(a.order||0)-Number(b.order||0);});
    if (!sellers.length) { root.innerHTML = '<p class="seller-empty">Seller profiles will be published here soon.</p>'; return; }
    var badges = Array.isArray(data.impactMetrics) ? data.impactMetrics : [];
    root.innerHTML = '<div class="seller-grid">' + sellers.map(function(seller){
      var href=safeHttps(seller.websiteUrl||seller.profileUrl), photo=seller.imageUrl?'<img src="'+esc(resolveImg(seller.imageUrl))+'" alt="'+esc(seller.name)+'" loading="lazy">':'<span>'+esc(initials(seller.name))+'</span>';
      var sellerBadges=(seller.badgeIds||[]).map(function(id){return badges.find(function(b){return b.id===id&&b.visible!==false;});}).filter(Boolean);
      var socials=Object.keys(seller.socialLinks||{}).map(function(name){var url=safeHttps(seller.socialLinks[name]);return url?'<a href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">'+esc(name.charAt(0).toUpperCase()+name.slice(1))+' ↗</a>':'';}).join('');
      return '<article class="seller-card"><div class="seller-photo">'+photo+'</div><div><p class="eyebrow">'+esc(seller.role||"Seller profile")+'</p><h3>'+esc(seller.name)+'</h3><p>'+esc(seller.biography||seller.description||"")+'</p>'
        +(sellerBadges.length?'<div class="seller-badges">'+sellerBadges.map(function(b){return '<span>'+esc(b.value||b.description)+'</span>';}).join('')+'</div>':'')
        +'<div class="seller-links">'+(seller.contactEmail?'<a href="mailto:'+esc(seller.contactEmail)+'">Email</a>':'')+(seller.contactPhone?'<a href="tel:'+esc(String(seller.contactPhone).replace(/[^+\d]/g,""))+'">Call</a>':'')+(href?'<a href="'+esc(href)+'" target="_blank" rel="noopener noreferrer">Website ↗</a>':'')+socials+'</div></div></article>';
    }).join('') + '</div>';
  }

  function renderBadges(data) {
    var root=document.querySelector('[data-render="badges"]'); if(!root)return;
    var badges=(Array.isArray(data.badges)?data.badges:[]).filter(function(b){return b&&b.visible!==false;}).sort(function(a,b){return Number(a.order||0)-Number(b.order||0);});
    var section=root.closest('[data-badge-section]'); if(section)section.hidden=!badges.length;
    root.innerHTML=badges.map(function(b){var href=safeHttps(b.linkUrl);var visual=b.imageUrl?'<img src="'+esc(resolveImg(b.imageUrl))+'" alt="" loading="lazy">':'<span aria-hidden="true">✦</span>';var body='<div class="badge-visual">'+visual+'</div><div><h3>'+esc(b.title)+'</h3>'+(b.description?'<p>'+esc(b.description)+'</p>':'')+'</div>';return href?'<a class="badge-card" href="'+esc(href)+'" target="_blank" rel="noopener noreferrer">'+body+'</a>':'<article class="badge-card">'+body+'</article>';}).join('');
  }

  function renderEditableIcons(data) {
    var icons=Array.isArray(data.icons)?data.icons:[];
    var targets={"waste-management":'a[href="waste-management.html"] .d-ic, a[href="waste-management.html"].init-card .icon-chip',"environmental-education":'a[href="education.html"] .d-ic, a[href="education.html"].init-card .icon-chip',"empowher":'a[href="empowher.html"] .d-ic, a[href="empowher.html"].init-card .icon-chip',"csr-partnerships":'a[href="csr-partnerships.html"] .d-ic, a[href="csr-partnerships.html"].init-card .icon-chip'};
    icons.filter(function(icon){return icon&&icon.visible!==false&&icon.imageUrl;}).forEach(function(icon){
      var selector=targets[icon.id]||('[data-icon-id="'+String(icon.id).replace(/[^A-Za-z0-9_-]/g,"")+'"]');
      document.querySelectorAll(selector).forEach(function(el){el.innerHTML='<img src="'+esc(resolveImg(icon.imageUrl))+'" alt="" loading="lazy">';el.classList.add("custom-icon");});
    });
  }

  function renderEducation(data) {
    var root = document.querySelector('[data-render="education"]');
    if (!root) return;
    var articles = Array.isArray(data.educationArticles) ? data.educationArticles : [];
    root.innerHTML = articles.map(function (article) {
      var href = safeHttps(article.linkUrl);
      var media = article.imageUrl
        ? '<div class="resource-media"><img src="' + esc(resolveImg(article.imageUrl)) + '" alt="' + esc(article.title) + '" loading="lazy" decoding="async"></div>'
        : '<div class="resource-media resource-placeholder"><span>Environmental learning</span></div>';
      return '<article class="resource-card">' + media + '<div class="resource-body"><h3>' + esc(article.title)
        + "</h3><p>" + esc(article.description) + "</p>"
        + (href ? '<a href="' + esc(href) + '" target="_blank" rel="noopener noreferrer">'
          + esc(article.linkLabel || "Learn more") + " ↗</a>" : "") + "</div></article>";
    }).join("");
  }

  function renderImpactMetrics(data) {
    var root = document.querySelector('[data-render="impact-metrics"]');
    if (!root) return;
    var metrics = (Array.isArray(data.impactMetrics) ? data.impactMetrics.slice() : []).filter(function(metric){return metric&&metric.visible!==false;}).sort(function(a,b){return Number(a.order||0)-Number(b.order||0);});
    var delays = ["", " reveal-d1", " reveal-d2"];
    root.innerHTML = metrics.map(function (metric, index) {
      var custom=metric.imageUrl?{imageUrl:metric.imageUrl}:(Array.isArray(data.icons)?data.icons:[]).find(function(item){return item&&item.id===metric.icon&&item.visible!==false&&item.imageUrl;});
      var icon = IMPACT_ICONS[metric.icon] || IMPACT_ICONS.recycle;
      return '<article class="impact-card reveal' + delays[index % 3] + '">'
        + '<span class="impact-icon" aria-hidden="true">' + (custom?'<img src="'+esc(resolveImg(custom.imageUrl))+'" alt="">':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' + icon + '</svg>') + '</span>'
        + '<b>' + esc(metric.value) + '</b><span>' + esc(metric.description) + '</span></article>';
    }).join("");
    window.requestAnimationFrame(function () {
      root.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); });
    });
  }

  var branchMap = null;
  function renderBranches(data) {
    var list = document.querySelector('[data-render="branches"]');
    var mapEl = document.getElementById("branchMap");
    if (!list && !mapEl) return;
    var branches = (Array.isArray(data.branches) ? data.branches : []).filter(function (branch) {
      return Number.isFinite(Number(branch.latitude)) && Number.isFinite(Number(branch.longitude));
    });
    if (list) {
      list.innerHTML = branches.map(function (branch, index) {
        return '<button class="branch-card" data-branch-index="' + index + '"><span class="branch-type">'
          + (branch.type === "main" ? "Main branch" : "Sub-branch") + "</span><strong>" + esc(branch.name)
          + "</strong><span>" + esc(branch.address) + "</span>"
          + (branch.contact ? "<small>" + esc(branch.contact) + "</small>" : "") + "</button>";
      }).join("") || "<p>No branch locations have been published yet.</p>";
    }
    if (!mapEl || !window.L || !branches.length) return;
    if (branchMap) branchMap.remove();
    branchMap = window.L.map(mapEl, { scrollWheelZoom: false });
    window.L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(branchMap);
    var bounds = [];
    var markers = branches.map(function (branch) {
      var latlng = [Number(branch.latitude), Number(branch.longitude)];
      bounds.push(latlng);
      var popup = document.createElement("div");
      var title = document.createElement("strong"); title.textContent = branch.name || "Reclaim Era branch";
      var address = document.createElement("p"); address.textContent = branch.address || "";
      popup.appendChild(title); popup.appendChild(address);
      if (branch.contact) { var contact = document.createElement("small"); contact.textContent = branch.contact; popup.appendChild(contact); }
      return window.L.marker(latlng, { title: branch.name || "Branch", alt: branch.name || "Branch" }).addTo(branchMap).bindPopup(popup);
    });
    branchMap.fitBounds(bounds, { padding: [34, 34], maxZoom: 14 });
    if (list) list.onclick = function (event) {
      var card = event.target.closest("[data-branch-index]");
      if (!card) return;
      var marker = markers[Number(card.getAttribute("data-branch-index"))];
      if (marker) { branchMap.setView(marker.getLatLng(), 15); marker.openPopup(); }
    };
  }

  /* ---------- apply a content object to the page ---------- */
  function apply(data, gallery) {
    document.querySelectorAll('[data-render="products"]').forEach(function (el) {
      renderProducts(el, data.products, {
        variant: el.getAttribute("data-variant") || "full",
        limit: parseInt(el.getAttribute("data-limit") || "0", 10),
        reveal: true
      });
    });
    var metricValues = {};
    (data.impactMetrics || []).forEach(function (metric) { if (metric && metric.id) metricValues[metric.id] = metric.value; });
    document.querySelectorAll("[data-stat]").forEach(function (el) {
      var key = el.getAttribute("data-stat");
      var v = metricValues[key] || (data.stats || {})[key];
      if (v) el.textContent = v;
    });
    if (data.phone) {
      document.querySelectorAll("[data-phone]").forEach(function (el) {
        el.textContent = data.phone;
        if (el.tagName === "A") el.href = "tel:" + String(data.phone).replace(/[^+\d]/g, "");
      });
    }
    var grid = document.getElementById("galleryGrid");
    if (grid) renderGallery(grid, gallery);
    renderTeam(data);
    renderSeller(data);
    renderBadges(data);
    renderEditableIcons(data);
    renderEducation(data);
    renderBranches(data);
    renderImpactMetrics(data);
  }

  /* ---------- resolve: static baseline, then published live content ---------- */
  var staticData = window.RE_DATA || {};
  var staticGallery = window.RE_GALLERY || [];

  var CACHE_KEY = "re-content-cache";
  var SYNC_CHANNEL = "reclaim-era-live-content";
  var liveChannel = null;

  function applyLive(live) {
    apply(
      {
        products: live.products || staticData.products,
        stats: live.stats || staticData.stats,
        phone: live.phone || staticData.phone,
        seller: live.seller || staticData.seller,
        sellers: live.sellers || staticData.sellers,
        badges: live.badges || staticData.badges,
        icons: live.icons || staticData.icons,
        team: live.team || staticData.team,
        educationArticles: live.educationArticles || staticData.educationArticles,
        branches: live.branches || staticData.branches,
        impactMetrics: live.impactMetrics || staticData.impactMetrics
      },
      live.gallery || staticGallery
    );
  }

  function cacheAndApply(live) {
    if (!live || !(live.products || live.stats || live.phone || live.gallery || live.team || live.seller || live.sellers || live.badges || live.icons || live.educationArticles || live.branches || live.impactMetrics)) return;
    applyLive(live);
    try { localStorage.setItem(CACHE_KEY, JSON.stringify(live)); } catch (e) {}
  }

  function refreshLive() {
    if (window.RE_HAS_BACKEND === false) return;
    fetch(API_BASE + "/api/content?fresh=" + Date.now(), {
      cache: "no-store",
      headers: { Accept: "application/json" }
    })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (live) {
        if (live && (live.products || live.stats || live.phone || live.gallery || live.team || live.seller || live.sellers || live.badges || live.icons || live.educationArticles || live.branches || live.impactMetrics)) {
          cacheAndApply(live);
        } else {
          try { localStorage.removeItem(CACHE_KEY); } catch (e) {}
        }
      })
      .catch(function () {});               // offline / no backend → keep static + cache
  }

  if (window.RE_HAS_BACKEND === false) {
    apply(staticData, staticGallery);       // pure-static: the files are the source of truth
  } else {
    apply(staticData, staticGallery);       // instant paint from static files
    // instant paint from a cached copy of the live content (fast repeat visits)
    try {
      var cached = JSON.parse(localStorage.getItem(CACHE_KEY));
      if (cached && (cached.products || cached.stats || cached.phone || cached.gallery || cached.team || cached.seller || cached.sellers || cached.badges || cached.icons || cached.educationArticles || cached.branches || cached.impactMetrics)) applyLive(cached);
    } catch (e) {}
    // Revalidate now, whenever the tab is revisited, and once per minute. An
    // admin save also pushes the same content instantly through BroadcastChannel
    // and localStorage to public pages open on this device.
    refreshLive();
    if ("BroadcastChannel" in window) {
      liveChannel = new BroadcastChannel(SYNC_CHANNEL);
      liveChannel.addEventListener("message", function (event) {
        cacheAndApply(event.data);
      });
    }
    window.addEventListener("storage", function (event) {
      if (event.key === CACHE_KEY && event.newValue) {
        try { cacheAndApply(JSON.parse(event.newValue)); } catch (e) {}
      }
    });
    document.addEventListener("visibilitychange", function () {
      if (!document.hidden) refreshLive();
    });
    window.setInterval(refreshLive, 30 * 1000);
  }

  /* gallery lightbox (bind once) */
  var grid = document.getElementById("galleryGrid");
  var lb = document.getElementById("galLightbox");
  if (grid && lb) {
    var previousFocus = null;
    var closeControl = lb.querySelector(".gal-lb-close");
    var closeLightbox = function () {
      lb.classList.remove("open");
      lb.setAttribute("aria-hidden", "true");
      if (previousFocus && previousFocus.focus) previousFocus.focus();
    };
    var openLightbox = function (card) {
      previousFocus = card;
      var image = lb.querySelector("img");
      image.src = card.getAttribute("data-full");
      image.alt = card.getAttribute("data-title") || "Gallery image";
      lb.querySelector(".gal-lb-cap").textContent = card.getAttribute("data-title") || "";
      lb.classList.add("open");
      lb.setAttribute("aria-hidden", "false");
      if (closeControl) closeControl.focus();
    };
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "Gallery image preview");
    lb.setAttribute("aria-hidden", "true");
    grid.addEventListener("click", function (e) {
      var c = e.target.closest(".gal-card.has-img");
      if (!c) return;
      openLightbox(c);
    });
    grid.addEventListener("keydown", function (event) {
      var c = event.target.closest(".gal-card.has-img");
      if (!c || (event.key !== "Enter" && event.key !== " ")) return;
      event.preventDefault();
      openLightbox(c);
    });
    lb.addEventListener("click", function (event) {
      if (event.target === lb || event.target === closeControl) closeLightbox();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && lb.classList.contains("open")) closeLightbox();
    });
  }

  /* expose for admin.html */
  window.RE_RENDER = {
    ART: ART,
    card: card,
    renderInto: renderProducts,
    esc: esc,
    PREVIEW_KEY: PREVIEW_KEY,
    CACHE_KEY: CACHE_KEY,
    SYNC_CHANNEL: SYNC_CHANNEL,
    API_BASE: API_BASE
  };
})();
