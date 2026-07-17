# -*- coding: utf-8 -*-
"""Builds the Reclaim Era static site into /Users/prajwal/reclaim era/website/"""
import os

OUT = "/Users/prajwal/reclaim era/website"

# ---------------------------------------------------------------- icons
I = {
"arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
"truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M14 17h-9V5h9zM14 8h4l3 4v5h-3"/><circle cx="7.5" cy="17.5" r="2"/><circle cx="16.5" cy="17.5" r="2"/></svg>',
"heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M19.5 12.6 12 20l-7.5-7.4a5 5 0 1 1 7.5-6.6 5 5 0 1 1 7.5 6.6Z"/></svg>',
"recycle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M7 19H4.8a1.8 1.8 0 0 1-1.6-2.7l1.9-3.2M14 19H9.5M17 19h2.2a1.8 1.8 0 0 0 1.6-2.7L19 13M15.5 7.6 13.4 4a1.8 1.8 0 0 0-3.1 0L8.5 7M15.5 7.6l4 6.9M15.5 7.6H11M5.1 13.1 8.5 7"/><path d="m5.1 13.1-2-1M8.5 7l-2.2-.5M19 13l2-.9"/></svg>',
"rise": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/></svg>',
"book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6c-2-1.5-4.5-2-8-2v14c3.5 0 6 .5 8 2 2-1.5 4.5-2 8-2V4c-3.5 0-6 .5-8 2Z"/><path d="M12 6v14"/></svg>',
"sew": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20c8 0 12-4 16-12"/><path d="M19 4l1 4-4-1z"/><path d="M4 20l3-1-2-2z"/><path d="M9.5 14.5l1.2 1.2M12.5 11.5l1.2 1.2M15 8.5l1.2 1.2" stroke-dasharray="2 2.6"/></svg>',
"handshake": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="m11 17 2 2a1.5 1.5 0 0 0 3-3"/><path d="m14 14 2.5 2.5a1.5 1.5 0 0 0 3-3l-4.8-4.8a2 2 0 0 0-2.8 0L10.5 10a1.6 1.6 0 0 1-2.3-2.3L11 4.9a4 4 0 0 1 5.6 0l4 4.1"/><path d="M3 9.5 8.5 4M3 14l4 4a1.5 1.5 0 0 0 3-3"/></svg>',
"leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M6 21c0-9 4-15 14-16 0 11-5 15-11 15-1.5 0-3-.5-3-.5"/><path d="M6 21c2-6 5-9 9-11"/></svg>',
"check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
"download": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11m0 0 4-4m-4 4-4-4M4 19h16"/></svg>',
"users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.4"/><path d="M2.8 20a6.2 6.2 0 0 1 12.4 0"/><path d="M15.5 4.9a3.4 3.4 0 0 1 0 6.2M17.8 14.6a6.2 6.2 0 0 1 3.4 5.4"/></svg>',
"shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 5 6v5c0 4.6 3 8.4 7 10 4-1.6 7-5.4 7-10V6Z"/><path d="m9 11.5 2 2 4-4"/></svg>',
"phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M6.6 3h3l1.5 4.5-2 1.5a12 12 0 0 0 5.9 5.9l1.5-2L21 14.4v3A2.6 2.6 0 0 1 18.4 20 15.4 15.4 0 0 1 4 5.6 2.6 2.6 0 0 1 6.6 3Z"/></svg>',
"mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/></svg>',
"pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11Z"/><circle cx="12" cy="10" r="2.6"/></svg>',
"gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="9" width="16" height="4"/><path d="M6 13v7h12v-7M12 9v11M12 9s-4 0-5-2 1-4 3-3 2 5 2 5Zm0 0s4 0 5-2-1-4-3-3-2 5-2 5Z"/></svg>',
"cart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4h2.5l2.2 11h10.6L21 7H6"/><circle cx="9.5" cy="19.5" r="1.6"/><circle cx="16.5" cy="19.5" r="1.6"/></svg>',
"spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3c.6 4.8 2.4 6.9 7 7.5-4.6.6-6.4 2.7-7 7.5-.6-4.8-2.4-6.9-7-7.5 4.6-.6 6.4-2.7 7-7.5Z"/><path d="M19 15.5c.3 2 1 2.8 3 3-2 .3-2.7 1-3 3-.3-2-1-2.7-3-3 2-.2 2.7-1 3-3Z"/></svg>',
"cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="5" width="16" height="16" rx="2.5"/><path d="M8 3v4M16 3v4M4 10h16"/></svg>',
"camera": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h3l2-2.5h6L17 8h3v11H4Z"/><circle cx="12" cy="13" r="3.2"/></svg>',
"file": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h8l4 4v14H6Z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></svg>',
"warn": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4 2.8 20h18.4Z"/><path d="M12 10v4.5M12 17.5v.1"/></svg>',
"trash": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M9 7V4h6v3M6.5 7l1 13h9l1-13"/></svg>',
"laptop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="4.5" y="5" width="15" height="10" rx="1.6"/><path d="M2.5 19h19"/></svg>',
"grad": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="m12 4 10 5-10 5L2 9Z"/><path d="M6 11.5V16c0 1.7 2.7 3 6 3s6-1.3 6-3v-4.5"/></svg>',
"ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".9" fill="currentColor" stroke="none"/></svg>',
"fb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 21v-7h2.8l.5-3.3h-3.3V8.5c0-1 .3-1.7 1.8-1.7h1.6V3.9c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.4-4 4.1v2.8H8.5V14h2.9v7Z"/></svg>',
"li": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M8 10.5V17M8 7.2v.1M12 17v-3.8c0-1.5 4-2.1 4 0V17"/></svg>',
}

# ------------------------------------------------------- product artwork
def tote(body="#3D5A99", light="#5C7BBD"):
    return f'''<svg viewBox="0 0 200 200" aria-hidden="true">
<circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/>
<circle cx="100" cy="104" r="86" fill="none" stroke="#00BF63" stroke-width="1.6" stroke-dasharray="5 7" opacity=".5"/>
<path d="M70 62 Q100 30 130 62" fill="none" stroke="#96543F" stroke-width="7" stroke-linecap="round"/>
<rect x="48" y="62" width="104" height="96" rx="12" fill="{body}"/>
<rect x="48" y="62" width="104" height="30" rx="12" fill="{light}"/>
<rect x="56" y="70" width="88" height="80" rx="8" fill="none" stroke="#fff" stroke-width="1.6" stroke-dasharray="4 5" opacity=".55"/>
<rect x="76" y="108" width="48" height="30" rx="5" fill="{light}"/>
<circle cx="100" cy="123" r="6" fill="#00BF63"/>
</svg>'''

BACKPACK = '''<svg viewBox="0 0 200 200" aria-hidden="true">
<circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/>
<circle cx="100" cy="104" r="86" fill="none" stroke="#0522C8" stroke-width="1.6" stroke-dasharray="5 7" opacity=".35"/>
<path d="M78 56 Q100 38 122 56" fill="none" stroke="#96543F" stroke-width="7" stroke-linecap="round"/>
<rect x="52" y="56" width="96" height="104" rx="26" fill="#5E4034"/>
<rect x="52" y="56" width="96" height="104" rx="26" fill="none" stroke="#F4E7E1" stroke-width="1.6" stroke-dasharray="4 5" opacity=".5"/>
<rect x="66" y="112" width="68" height="48" rx="14" fill="#96543F"/>
<rect x="90" y="128" width="20" height="10" rx="4" fill="#E8B84B"/>
<path d="M66 88 h68" stroke="#F4E7E1" stroke-width="2" stroke-dasharray="4 5" opacity=".6"/>
<circle cx="100" cy="74" r="5" fill="#00BF63"/>
</svg>'''

ORGANIZER = '''<svg viewBox="0 0 200 200" aria-hidden="true">
<circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/>
<circle cx="100" cy="104" r="86" fill="none" stroke="#96543F" stroke-width="1.6" stroke-dasharray="5 7" opacity=".4"/>
<rect x="46" y="58" width="108" height="92" rx="10" fill="#2E4B8F"/>
<rect x="46" y="58" width="108" height="92" rx="10" fill="none" stroke="#fff" stroke-width="1.6" stroke-dasharray="4 5" opacity=".5"/>
<rect x="120" y="58" width="34" height="92" rx="10" fill="#3D5A99"/>
<rect x="132" y="86" width="10" height="36" rx="5" fill="#96543F"/>
<rect x="58" y="74" width="44" height="6" rx="3" fill="#E8EBFB" opacity=".85"/>
<rect x="58" y="88" width="32" height="6" rx="3" fill="#E8EBFB" opacity=".55"/>
<circle cx="64" cy="136" r="6" fill="#00BF63"/>
</svg>'''

BUNDLE = '''<svg viewBox="0 0 200 200" aria-hidden="true">
<circle cx="100" cy="104" r="86" fill="rgba(23,37,30,.045)"/>
<circle cx="100" cy="104" r="86" fill="none" stroke="#E8B84B" stroke-width="1.6" stroke-dasharray="5 7" opacity=".55"/>
<rect x="50" y="86" width="100" height="72" rx="10" fill="#0D3B28"/>
<rect x="50" y="86" width="100" height="20" rx="10" fill="#14532F"/>
<rect x="93" y="86" width="14" height="72" fill="#E8B84B"/>
<path d="M100 86 C 80 78 76 58 92 56 C 102 55 102 72 100 86 C 98 72 98 55 108 56 C 124 58 120 78 100 86Z" fill="#96543F"/>
<circle cx="100" cy="86" r="6" fill="#00BF63"/>
<rect x="50" y="86" width="100" height="72" rx="10" fill="none" stroke="#fff" stroke-width="1.4" stroke-dasharray="4 5" opacity=".35"/>
</svg>'''

# ---------------------------------------------------------------- shell
FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'''

def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" type="image/png" href="assets/favicon.png">
{FONTS}
<link rel="stylesheet" href="css/style.css">
</head>
<body>'''

def dropdown_tile(href, ic, chip, title, sub):
    return f'''<a href="{href}"><span class="d-ic {chip}">{ic}</span><span><b>{title}</b><span>{sub}</span></span></a>'''

def header(active=""):
    def cls(k):
        return ' class="nav-link active"' if k == active else ' class="nav-link"'
    tiles = (
        dropdown_tile("waste-management.html", I["recycle"], "bg-green-t", "Waste Management", "Textile recovery, zero landfill"),
        dropdown_tile("education.html", I["book"], "bg-blue-t", "Education (NEP 2020)", "Hands-on environmental curriculum"),
        dropdown_tile("empowher.html", I["sew"], "bg-terra-t", "EmpowHer Academy", "13 green livelihoods created"),
        dropdown_tile("csr-partnerships.html", I["handshake"], "bg-gold-t", "CSR Partnerships", "Verified ESG outcomes for corporates"),
    )
    init_active = ' class="nav-link active"' if active == "initiatives" else ' class="nav-link"'
    return f'''
<div class="utility">
  <div class="wrap">
    <span class="u-left">Kogilu Hub, Bengaluru · An initiative of Lamp Educational and Charitable Trust (LEACT)</span>
    <div class="u-right"><span>Donations <b>12A &amp; 80G</b> exempt</span><span>EN · ಕನ್ನಡ</span></div>
  </div>
</div>
<header class="header">
  <div class="wrap">
    <a href="index.html" class="brand" aria-label="Reclaim Era home">
      <span><span class="wordmark">re<span class="k">cla</span><span class="di">&#305;<i></i></span><span class="k">m</span> <span class="t">era</span><span class="dot">.</span></span>
      <small>Revive. Recycle. Rise.</small></span>
    </a>
    <ul class="nav" id="nav">
      <li><a{cls("about")} href="about.html">About</a></li>
      <li class="has-dropdown">
        <button{init_active} aria-expanded="false">Initiatives <span class="caret"></span></button>
        <div class="dropdown">{tiles[0]}{tiles[1]}{tiles[2]}{tiles[3]}</div>
      </li>
      <li><a{cls("shop")} href="shop.html">Shop</a></li>
      <li><a{cls("zero")} href="zero-waste-certification.html">Zero Waste</a></li>
      <li><a{cls("involved")} href="get-involved.html">Get Involved</a></li>
      <li><a{cls("resources")} href="resources.html">Resources</a></li>
      <li><a{cls("contact")} href="contact.html">Contact</a></li>
    </ul>
    <div class="header-cta">
      <a href="get-involved.html#donate" class="btn btn-terra btn-sm btn-donate-top">Donate</a>
      <a href="request-pickup.html" class="btn btn-green btn-sm">Request Pick-Up</a>
      <button class="nav-toggle" aria-label="Menu" aria-expanded="false">
        <svg class="icon-burger" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    </div>
  </div>
</header>
<div class="mobile-bar">
  <a href="request-pickup.html" class="mb-pickup">Pick-Up</a>
  <a href="get-involved.html#donate" class="mb-donate">Donate</a>
  <a href="shop.html" class="mb-shop">Shop</a>
</div>'''

FOOTER = f'''
<footer class="footer">
  <div class="footer-cta">
    <div class="wrap">
      <h3>Get monthly <em>impact reports</em> &amp; event invites.</h3>
      <form class="newsletter" action="https://formsubmit.co/reclaimera@gmail.com" method="POST">
        <input type="hidden" name="_subject" value="New newsletter signup (reclaimera.in)"><input type="hidden" name="form_type" value="Newsletter signup"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_template" value="table"><input type="text" name="_honey" style="display:none" tabindex="-1" aria-hidden="true">
        <input type="email" name="email" placeholder="Your email address" aria-label="Email address" required>
        <button class="btn btn-green" type="submit">Subscribe</button>
        <div class="form-success" role="status"><span>Thank you, you are subscribed. See you in the next report!</span></div>
        <div class="form-error" role="alert"><span data-msg>Could not subscribe right now. Please try again in a minute.</span></div>
      </form>
    </div>
  </div>
  <div class="footer-main">
    <div class="wrap">
      <div class="footer-brand">
        <span class="wordmark wm-light">re<span class="k">cla</span><span class="di">&#305;<i></i></span><span class="k">m</span> <span class="t">era</span><span class="dot">.</span></span>
        <p>We transform Bengaluru's discarded textiles and household items into education, green livelihoods, and a cleaner environment.</p>
        <div class="sdg-row" style="margin-top:18px">
          <span class="sdg s4">SDG 4</span><span class="sdg s8">SDG 8</span><span class="sdg s12">SDG 12</span><span class="sdg s13">SDG 13</span>
        </div>
        <div class="social-row">
          <a href="#" aria-label="Instagram">{I["ig"]}</a>
          <a href="#" aria-label="Facebook">{I["fb"]}</a>
          <a href="#" aria-label="LinkedIn">{I["li"]}</a>
        </div>
      </div>
      <div>
        <h5>Explore</h5>
        <ul class="footer-links">
          <li><a href="about.html">About Us</a></li>
          <li><a href="shop.html">Shop With Purpose</a></li>
          <li><a href="request-pickup.html">Request a Pick-Up</a></li>
          <li><a href="campaign-application.html">Host a Campaign</a></li>
          <li><a href="zero-waste-certification.html">Zero Waste Certification</a></li>
          <li><a href="resources.html">Resources</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h5>Initiatives</h5>
        <ul class="footer-links">
          <li><a href="waste-management.html">Waste Management</a></li>
          <li><a href="education.html">Education (NEP 2020)</a></li>
          <li><a href="empowher.html">EmpowHer Academy</a></li>
          <li><a href="csr-partnerships.html">CSR Partnerships</a></li>
        </ul>
      </div>
      <div>
        <h5>Get Involved</h5>
        <ul class="footer-links">
          <li><a href="get-involved.html#volunteer">Volunteer</a></li>
          <li><a href="get-involved.html#partner">Partner (CSR)</a></li>
          <li><a href="get-involved.html#donate">Donate</a></li>
          <li><a href="get-involved.html#donate-equipment">Donate Equipment</a></li>
        </ul>
      </div>
      <div>
        <h5>Reach Us</h5>
        <ul class="footer-links">
          <li>Kogilu Hub, Yelahanka,<br>Bengaluru, Karnataka</li>
          <li><a href="mailto:reclaimera@gmail.com">reclaimera@gmail.com</a></li>
          <li><a href="tel:+918152020145" data-phone>+91 81520 20145</a></li>
          <li><a href="tel:+917483042681">+91 74830 42681</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="wrap">
      <span>© <span data-year></span> Reclaim Era · Lamp Educational and Charitable Trust (LEACT). Donations eligible under sections 12A &amp; 80G.</span>
      <span><a href="privacy-policy.html">Privacy</a> &nbsp;·&nbsp; <a href="terms.html">Terms</a> &nbsp;·&nbsp; <a href="refund-policy.html">Refunds</a> &nbsp;·&nbsp; <a href="resources.html">Media Kit</a></span>
    </div>
  </div>
</footer>
<script src="js/site-data.js"></script>
<script src="js/render.js"></script>
<script src="js/main.js"></script>
</body>
</html>'''

def page_hero(crumb, h1, lede, ctas=""):
    return f'''
<section class="page-hero">
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span class="sep">/</span>{crumb}</nav>
    <h1 class="reveal">{h1}</h1>
    <p class="lede reveal reveal-d1">{lede}</p>
    {f'<div class="hero-ctas reveal reveal-d2">{ctas}</div>' if ctas else ''}
  </div>
</section>'''

def cta_band(h2, p, ctas):
    return f'''
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="cta-band reveal">
      <h2>{h2}</h2>
      <p>{p}</p>
      <div class="hero-ctas">{ctas}</div>
    </div>
  </div>
</section>'''

def feat(ic, chip, title, body, delay=""):
    return f'''<div class="feat-card reveal {delay}"><div class="icon-chip {chip}">{ic}</div><h4>{title}</h4><p>{body}</p></div>'''

# ================================================================ HOME
home_body = f'''
<section class="hero">
  <div class="wrap">
    <div>
      <p class="eyebrow reveal">Revive. Recycle. Rise.</p>
      <h1 class="reveal reveal-d1">Waste <span class="accent-t">to</span><br><span class="accent-i">Wisdom.</span></h1>
      <p class="lede reveal reveal-d2">We turn Bengaluru's discarded textiles and household items into <b>education</b>, <b>green livelihoods</b>, and a cleaner city, one pick-up at a time.</p>
      <div class="hero-ctas reveal reveal-d3">
        <a href="request-pickup.html" class="btn btn-green btn-lg">Request a Pick-Up {I["arrow"]}</a>
        <a href="shop.html" class="btn btn-outline btn-lg">Shop &amp; Support</a>
      </div>
    </div>
    <div class="hero-visual reveal reveal-d2">
      <div class="orbit">
        <svg class="spin-text" viewBox="0 0 200 200" aria-hidden="true">
          <defs><path id="circ" d="M100,100 m-90,0 a90,90 0 1,1 180,0 a90,90 0 1,1 -180,0"/></defs>
          <text><textPath href="#circ">REVIVE&#160;·&#160;RECYCLE&#160;·&#160;RISE&#160;·&#160;RECLAIM&#160;ERA&#160;·&#160;REVIVE&#160;·&#160;RECYCLE&#160;·&#160;RISE&#160;·&#160;</textPath></text>
        </svg>
        <div class="ring-outer"></div>
        <div class="ring-mid"></div>
        <div class="logo-disc"><img src="assets/logo.png" alt="Reclaim Era logo. Revive. Recycle. Rise."></div>
        <div class="stat-chip c1"><span class="n" data-stat="items">22K+</span><span class="l">items diverted<br>&amp; donated</span></div>
        <div class="stat-chip c2"><span class="n" data-stat="livelihoods">13</span><span class="l">green livelihoods<br>created</span></div>
        <div class="stat-chip c3"><span class="n" data-stat="schools">11</span><span class="l">government<br>schools reached</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow">How we work</p>
      <h2>From doorstep to <span style="color:var(--green-deep)">classroom</span>, nothing is wasted.</h2>
      <p>Four verbs power everything we do. Together they form a closed loop that turns clutter into learning.</p>
    </div>
    <div class="steps-grid">
      <div class="step-card reveal"><span class="step-num">01</span><div class="icon-chip bg-blue-t">{I["truck"]}</div><h3>We Collect</h3><p>Hyper-local pickups, corporate collection drives, and campus Revive Stations across Bengaluru.</p></div>
      <div class="step-card reveal reveal-d1"><span class="step-num">02</span><div class="icon-chip bg-terra-t">{I["heart"]}</div><h3>We Revive</h3><p>Wearable items are sanitised and donated to BPL families and transit communities in need.</p></div>
      <div class="step-card reveal reveal-d2"><span class="step-num">03</span><div class="icon-chip bg-green-t">{I["recycle"]}</div><h3>We Recycle</h3><p>Unusable fabrics are diverted to industrial shredders, so nothing we collect goes to landfill.</p></div>
      <div class="step-card reveal reveal-d3"><span class="step-num">04</span><div class="icon-chip bg-gold-t">{I["rise"]}</div><h3>We Rise</h3><p>Heavy fabrics are upcycled into premium products; proceeds fund LEACT's education programs.</p></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Our initiatives</p>
      <h2>Four pillars, one circular economy.</h2>
      <p>Infrastructure, education, and livelihoods working together across Bengaluru.</p>
    </div>
    <div class="init-grid">
      <a href="waste-management.html" class="init-card t-green reveal">
        <div class="icon-chip bg-green-t">{I["recycle"]}</div>
        <span class="metric">22,000+ items diverted</span>
        <h3>Waste Management</h3>
        <p>An end-to-end textile recovery factory at the Kogilu hub: sorting, upcycling and downcycling, with zero landfill.</p>
        <span class="arrow-btn">{I["arrow"]}</span>
      </a>
      <a href="education.html" class="init-card t-blue reveal reveal-d1">
        <div class="icon-chip bg-blue-t">{I["book"]}</div>
        <span class="metric">11 schools · NEP 2020</span>
        <h3>Environmental Education</h3>
        <p>A year-long, hands-on curriculum with student-led audits and on-campus Revive Stations.</p>
        <span class="arrow-btn">{I["arrow"]}</span>
      </a>
      <a href="empowher.html" class="init-card t-terra reveal reveal-d2">
        <div class="icon-chip bg-terra-t">{I["sew"]}</div>
        <span class="metric">13 livelihoods created</span>
        <h3>EmpowHer Upcycling Academy</h3>
        <p>Women artisans trained in tailoring, digital skills and e-commerce, where tradition meets technology.</p>
        <span class="arrow-btn">{I["arrow"]}</span>
      </a>
      <a href="csr-partnerships.html" class="init-card t-gold reveal reveal-d3">
        <div class="icon-chip bg-gold-t">{I["handshake"]}</div>
        <span class="metric">20 corporate programs</span>
        <h3>CSR Partnerships</h3>
        <p>Tailored corporate programs that convert waste into verified ESG outcomes and employee engagement.</p>
        <span class="arrow-btn">{I["arrow"]}</span>
      </a>
    </div>
  </div>
</section>

<section class="section milestones">
  <div class="giant-year">2030</div>
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Our 2030 milestones</p>
      <h2>Where we're headed.</h2>
      <p>Six commitments that keep us accountable for the decade.</p>
    </div>
    <div class="mile-grid">
      <div class="mile reveal"><span class="tick">{I["check"]}</span><span><b>800,000 items</b><span>collected and diverted from landfill</span></span></div>
      <div class="mile reveal reveal-d1"><span class="tick">{I["check"]}</span><span><b>120 green livelihoods</b><span>created for women artisans</span></span></div>
      <div class="mile reveal reveal-d2"><span class="tick">{I["check"]}</span><span><b>1,600 students</b><span>receiving environmental education</span></span></div>
      <div class="mile reveal"><span class="tick">{I["check"]}</span><span><b>60 government schools</b><span>supplied with board games &amp; toys</span></span></div>
      <div class="mile reveal reveal-d1"><span class="tick">{I["check"]}</span><span><b>60 corporate programs</b><span>of employee-led volunteering</span></span></div>
      <div class="mile reveal reveal-d2"><span class="tick">{I["check"]}</span><span><b>30,000 notebooks</b><span>distributed to students in need</span></span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow">Quick actions</p>
      <h2>Three ways to start <span style="color:var(--terra)">today.</span></h2>
    </div>
    <div class="action-grid">
      <a href="zero-waste-certification.html" class="action-card a-green reveal">
        <span class="tag">For RWAs &amp; corporates</span>
        <h3>Book a Waste Audit</h3>
        <p>Turn your campus into a zero-waste campus with a free baseline audit.</p>
        <span class="fake-btn">Book a Waste Audit {I["arrow"]}</span>
      </a>
      <a href="education.html" class="action-card a-blue reveal reveal-d1">
        <span class="tag">For schools</span>
        <h3>Partner Your School</h3>
        <p>Bring the NEP 2020-aligned environmental curriculum to your students.</p>
        <span class="fake-btn">Partner Your School {I["arrow"]}</span>
      </a>
      <a href="shop.html" class="action-card a-terra reveal reveal-d2">
        <span class="tag">For everyone</span>
        <h3>Visit the Upcycle Shop</h3>
        <p>Buy handcrafted products that directly fund children's education.</p>
        <span class="fake-btn">Visit Shop {I["arrow"]}</span>
      </a>
    </div>
  </div>
</section>

<section class="section" style="background:var(--cream-2)">
  <div class="wrap">
    <div class="section-head" style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:18px 24px;max-width:none">
      <div>
        <p class="eyebrow">Shop with purpose</p>
        <h2>Every purchase funds a teacher.</h2>
        <p style="color:var(--ink-soft);margin-top:10px">20% of proceeds go to teacher salaries and school infrastructure through LEACT.</p>
      </div>
      <a href="shop.html" class="text-link">Browse all products {I["arrow"]}</a>
    </div>
    <div class="prod-grid" data-render="products" data-variant="teaser" data-limit="4"></div>
  </div>
</section>
'''

# JSON-LD for home
HOME_LD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "NGO",
  "name": "Reclaim Era",
  "alternateName": "Lamp Educational and Charitable Trust (LEACT)",
  "slogan": "Waste to Wisdom. Revive. Recycle. Rise.",
  "areaServed": "Bengaluru, Karnataka, India",
  "email": "reclaimera@gmail.com",
  "description": "Reclaim Era turns Bengaluru's textile waste into education and dignified livelihoods. Request a pickup, partner for CSR, or shop upcycled products."
}
</script>'''

# ================================================================ ABOUT
about_body = page_hero(
    '<a href="about.html">About Us</a>',
    'Our <span style="color:var(--green-deep)">story.</span>',
    "From local collection drives to a dedicated Kogilu hub, turning waste into resources for education and livelihoods.",
    f'<a href="resources.html" class="btn btn-green">Read Our Impact Report {I["arrow"]}</a>'
) + f'''
<section class="section" style="padding-top:40px">
  <div class="wrap two-col">
    <div class="prose reveal">
      <p class="eyebrow">Origin &amp; mission</p>
      <h3>Two urgent problems. One local answer.</h3>
      <p>Reclaim Era began to solve two problems at once: <b>overflowing textile waste</b> in Bengaluru and <b>underfunded education</b> for children.</p>
      <p>We built a local processing hub in Kogilu to collect, sort, and transform discarded textiles into direct relief and revenue for schools. Practical waste infrastructure meets behavioural education, supporting Bengaluru's vision of a landfill-free city.</p>
      <ul class="check-list">
        <li><span><b>Local first.</b> Collection, sorting, and processing all happen inside the city.</span></li>
        <li><span><b>Radically transparent.</b> Every rupee of proceeds is routed to LEACT and reported.</span></li>
        <li><span><b>Dignity-driven.</b> Livelihoods, not charity. We train women artisans into entrepreneurs.</span></li>
      </ul>
    </div>
    <div class="reveal reveal-d1">
      <p class="eyebrow">Milestones</p>
      <div class="timeline">
        <div class="tl-item"><b>The first drives</b><span>Neighbourhood collection drives prove that Bengaluru wants a better destination for its textiles.</span></div>
        <div class="tl-item"><b>Kogilu hub opens</b><span>A dedicated processing centre for sorting, sanitising, and upcycling at scale.</span></div>
        <div class="tl-item"><b>22,000+ items diverted</b><span>Wearables donated to BPL families and transit communities; the rest recycled, with zero landfill.</span></div>
        <div class="tl-item"><b>11 schools reached</b><span>The NEP 2020-aligned environmental curriculum enters government classrooms.</span></div>
        <div class="tl-item"><b>13 livelihoods created</b><span>The EmpowHer Academy graduates its first women artisans into stable green work.</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--cream-2)">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow">The dual impact model</p>
      <h2>One stream of waste, <span style="color:var(--terra)">three streams of good.</span></h2>
    </div>
    <div class="feat-grid">
      {feat(I["heart"], "bg-terra-t", "Revive", "Sanitise and donate wearable items to BPL families and transit communities across the city.")}
      {feat(I["sew"], "bg-blue-t", "EmpowHer", "Train women in tailoring and digital skills to create dignified, stable livelihoods.", "reveal-d1")}
      {feat(I["rise"], "bg-green-t", "Recycle &amp; Rise", "Divert unusable fabrics to industrial recycling and upcycle heavy fabrics into premium products that fund education.", "reveal-d2")}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow">Team &amp; board</p>
      <h2>The people behind the pick-ups.</h2>
    </div>
    <div class="team-grid">
      <div class="team-card reveal">
        <div class="avatar" style="background:linear-gradient(140deg,var(--blue),#02157e)">JR</div>
        <h4>Jaganathan Rajagopal</h4>
        <p class="role" style="color:var(--blue)">Founder &amp; CEO</p>
        <p>Building the bridge between Bengaluru's waste problem and its education gap.</p>
      </div>
      <div class="team-card reveal reveal-d1">
        <div class="avatar" style="background:linear-gradient(140deg,var(--green),#066B3C)">DT</div>
        <h4>Divya Tejaswini</h4>
        <p class="role" style="color:var(--green-deep)">Head of Networking &amp; Outreach</p>
        <p>Connecting RWAs, campuses, and corporates into one collection network.</p>
      </div>
      <div class="team-card reveal reveal-d2">
        <div class="avatar" style="background:linear-gradient(140deg,var(--terra),#6E3A29)">SR</div>
        <h4>Smitha Rajarathinam</h4>
        <p class="role" style="color:var(--terra)">Head of Finance &amp; Sales</p>
        <p>Keeping every rupee accountable, from shop sales to teacher salaries.</p>
      </div>
    </div>
  </div>
</section>
''' + cta_band(
    'See the numbers behind the <em>mission.</em>',
    "Our annual impact report covers items diverted, livelihoods created, and every rupee routed to education.",
    f'<a href="resources.html" class="btn btn-green btn-lg">Read Our Impact Report {I["arrow"]}</a><a href="contact.html" class="btn btn-outline-light btn-lg">Talk to Us</a>'
)

# ================================================================ INITIATIVES LANDING
initiatives_body = page_hero(
    '<span>Our Initiatives</span>',
    'Our <span style="color:var(--green-deep)">initiatives.</span>',
    "Practical programs that close the loop, from collection to classroom. Four pillars combining infrastructure, education, and livelihoods to create a decentralised circular economy across Bengaluru."
) + f'''
<section class="section" style="padding-top:30px">
  <div class="wrap">
    <div class="init-grid">
      <a href="waste-management.html" class="init-card t-green reveal">
        <div class="icon-chip bg-green-t">{I["recycle"]}</div>
        <span class="metric">Operations</span>
        <h3>Waste Management</h3>
        <p>End-to-end textile recovery at the Kogilu hub: sorting, upcycling, and downcycling to ensure zero landfill and measurable impact.</p>
        <span class="arrow-btn">{I["arrow"]}</span>
      </a>
      <a href="education.html" class="init-card t-blue reveal reveal-d1">
        <div class="icon-chip bg-blue-t">{I["book"]}</div>
        <span class="metric">Education</span>
        <h3>Environmental Education (NEP 2020)</h3>
        <p>A one-year hands-on curriculum aligned to NEP 2020 and NCF 2023: workshops, student-led audits, and on-campus Revive Stations.</p>
        <span class="arrow-btn">{I["arrow"]}</span>
      </a>
      <a href="empowher.html" class="init-card t-terra reveal reveal-d2">
        <div class="icon-chip bg-terra-t">{I["sew"]}</div>
        <span class="metric">Livelihoods</span>
        <h3>EmpowHer (Upcycling Academy)</h3>
        <p>Training women in tailoring, digital literacy, and e-commerce to create premium upcycled products and stable livelihoods.</p>
        <span class="arrow-btn">{I["arrow"]}</span>
      </a>
      <a href="csr-partnerships.html" class="init-card t-gold reveal reveal-d3">
        <div class="icon-chip bg-gold-t">{I["handshake"]}</div>
        <span class="metric">Corporate</span>
        <h3>CSR Partnerships</h3>
        <p>Tailored CSR programs that convert corporate waste into verified ESG outcomes, employee engagement, and measurable impact.</p>
        <span class="arrow-btn">{I["arrow"]}</span>
      </a>
    </div>
  </div>
</section>
''' + cta_band(
    'Not sure where to <em>start?</em>',
    "Tell us whether you are a resident, a school or a company and we will route you to the right program in one call.",
    f'<a href="contact.html" class="btn btn-green btn-lg">Talk to Us {I["arrow"]}</a><a href="request-pickup.html" class="btn btn-outline-light btn-lg">Request a Pick-Up</a>'
)

# ================================================================ WASTE MANAGEMENT
waste_body = page_hero(
    '<a href="initiatives.html">Our Initiatives</a><span class="sep">/</span><span>Waste Management</span>',
    'The textile &amp; household <span style="color:var(--green-deep)">recovery factory.</span>',
    "Reinventing how waste flows through our economy: scalable, traceable and zero waste at the Kogilu hub.",
    f'<a href="request-pickup.html" class="btn btn-green">Request a Pick-Up {I["arrow"]}</a><a href="zero-waste-certification.html" class="btn btn-outline">Book a Corporate Waste Audit</a>'
) + f'''
<section class="section" style="padding-top:40px">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Core processes</p>
      <h2>Every item gets a second act.</h2>
    </div>
    <div class="feat-grid">
      {feat(I["spark"], "bg-blue-t", "Sorting &amp; Segregation", "Every item that arrives at Kogilu is evaluated and triaged as wearable, upcyclable or recyclable.")}
      {feat(I["sew"], "bg-terra-t", "Upcycling", "Durable, heavy fabrics become premium products in the hands of EmpowHer artisans.", "reveal-d1")}
      {feat(I["recycle"], "bg-green-t", "Downcycling", "Heavily soiled items are processed into industrial inputs, so nothing goes to landfill.", "reveal-d2")}
    </div>
  </div>
</section>

<section class="section" style="background:var(--cream-2)">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The journey</p>
      <h2>From your doorstep to impact, in four steps.</h2>
    </div>
    <div class="journey">
      <div class="j-step reveal"><h4>Hyper-local collection</h4><p>Drop-offs, neighbourhood drives, and campus Revive Stations across Bengaluru.</p></div>
      <div class="j-step reveal reveal-d1"><h4>Sorting &amp; triage</h4><p>Items are evaluated at the Kogilu hub and routed by condition and material.</p></div>
      <div class="j-step reveal reveal-d2"><h4>Revive / Recycle / Rise</h4><p>Donated to communities, diverted to shredders, or upcycled into products.</p></div>
      <div class="j-step reveal reveal-d3"><h4>Sales &amp; impact routing</h4><p>Proceeds flow to LEACT to fund teachers, notebooks and school infrastructure.</p></div>
    </div>
  </div>
</section>
''' + cta_band(
    'Got a cupboard full of <em>maybe-someday?</em>',
    "Schedule a contactless pick-up and we will make sure every item finds its most useful second life.",
    f'<a href="request-pickup.html" class="btn btn-green btn-lg">Request a Pick-Up {I["arrow"]}</a><a href="zero-waste-certification.html" class="btn btn-outline-light btn-lg">Book a Corporate Waste Audit</a>'
)

# ================================================================ EDUCATION
education_body = page_hero(
    '<a href="initiatives.html">Our Initiatives</a><span class="sep">/</span><span>Education (NEP 2020)</span>',
    'Environmental education, <span style="color:var(--blue)">hands-on.</span>',
    "Move from textbook theory to real-world action with a year-long curriculum aligned to NEP 2020 and NCF 2023.",
    f'<a href="contact.html" class="btn btn-green">Partner Your School {I["arrow"]}</a>'
) + f'''
<section class="section" style="padding-top:40px">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Program components</p>
      <h2>A curriculum that gets its hands dirty.</h2>
    </div>
    <div class="feat-grid">
      {feat(I["spark"], "bg-blue-t", "Interactive workshops", "Project-based learning that turns waste literacy into a school-year adventure.")}
      {feat(I["shield"], "bg-green-t", "Student-led Zero Waste Audits", "Students audit their own campus and run on-site Revive Stations.", "reveal-d1")}
      {feat(I["grad"], "bg-terra-t", "Teacher training", "Educators get full training and materials, aligned to NEP 2020 &amp; NCF 2023.", "reveal-d2")}
    </div>
  </div>
</section>

<section class="section" style="background:var(--cream-2)">
  <div class="wrap two-col">
    <div class="prose reveal">
      <p class="eyebrow">Why it works</p>
      <h3>Behaviour change starts in the classroom.</h3>
      <p>Our one-year program embeds circular thinking into daily school life. Students don't just learn about waste. They <b>weigh it, sort it and divert it</b>, then teach their families to do the same.</p>
      <ul class="check-list">
        <li><span><b>11 government schools</b> already partnered across Bengaluru.</span></li>
        <li><span><b>1,600 students</b> targeted for environmental education by 2030.</span></li>
        <li><span><b>Board games, toys and notebooks</b> supplied to classrooms, funded by the upcycle shop.</span></li>
      </ul>
    </div>
    <div class="reveal reveal-d1">
      <div class="info-panel" style="position:static">
        <h3>What your school receives</h3>
        <ul>
          <li>{I["check"]}<span>A 1-year, ready-to-run environmental curriculum</span></li>
          <li>{I["check"]}<span>On-campus Revive Station set-up and signage</span></li>
          <li>{I["check"]}<span>Teacher training and ongoing support</span></li>
          <li>{I["check"]}<span>Student zero-waste audit toolkits</span></li>
          <li>{I["check"]}<span>End-of-year impact certificate for the school</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>
''' + cta_band(
    'Bring the program to <em>your school.</em>',
    "NEP 2020-aligned, teacher-friendly, and loved by students. Onboarding takes under two weeks.",
    f'<a href="contact.html" class="btn btn-green btn-lg">Partner Your School {I["arrow"]}</a>'
)

# ================================================================ EMPOWHER
empowher_body = page_hero(
    '<a href="initiatives.html">Our Initiatives</a><span class="sep">/</span><span>EmpowHer</span>',
    'EmpowHer, the women-led <span style="color:var(--terra)">upcycling academy.</span>',
    "Tradition meets technology: training, digital skills, and market access for women artisans.",
    f'<a href="shop.html" class="btn btn-terra">Shop With Purpose {I["arrow"]}</a><a href="get-involved.html#partner" class="btn btn-outline">Sponsor a Training Batch</a>'
) + f'''
<section class="section" style="padding-top:40px">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Curriculum &amp; skills</p>
      <h2>From first stitch to first sale.</h2>
    </div>
    <div class="feat-grid">
      {feat(I["sew"], "bg-terra-t", "Craft &amp; production", "Tailoring and dress design, industrial stitching, and pattern making to a premium standard.")}
      {feat(I["laptop"], "bg-blue-t", "Digital &amp; AI literacy", "Digital tools for fashion, e-commerce and marketing. Artisans run their own listings.", "reveal-d1")}
      {feat(I["rise"], "bg-green-t", "Business &amp; life skills", "Soft skills, financial literacy, and business management for lasting independence.", "reveal-d2")}
    </div>
  </div>
</section>

<section class="section" style="background:var(--cream-2)">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow">Stories of change</p>
      <h2>13 livelihoods and counting.</h2>
    </div>
    <div class="feat-grid">
      <div class="feat-card reveal" style="border-top:4px solid var(--terra)">
        <p style="font-family:var(--font-display);font-weight:600;font-size:1.05rem;color:var(--ink);margin-bottom:14px">"The first thing I bought with my own earnings was a school bag for my daughter, one I stitched myself."</p>
        <p style="font-size:.85rem"><b style="color:var(--ink)">EmpowHer artisan</b> · Batch 1, Kogilu hub</p>
      </div>
      <div class="feat-card reveal reveal-d1" style="border-top:4px solid var(--blue)">
        <p style="font-family:var(--font-display);font-weight:600;font-size:1.05rem;color:var(--ink);margin-bottom:14px">"I came for the sewing machine. I stayed for the laptop. Now I photograph and list my own products."</p>
        <p style="font-size:.85rem"><b style="color:var(--ink)">EmpowHer artisan</b> · Digital skills track</p>
      </div>
      <div class="feat-card reveal reveal-d2" style="border-top:4px solid var(--green)">
        <p style="font-family:var(--font-display);font-weight:600;font-size:1.05rem;color:var(--ink);margin-bottom:14px">"Denim that people threw away pays my rent now. Nothing is waste. That is what we prove every day."</p>
        <p style="font-size:.85rem"><b style="color:var(--ink)">EmpowHer artisan</b> · Production lead</p>
      </div>
    </div>
    <p style="text-align:center;margin-top:30px;color:var(--ink-soft);font-size:.9rem">Impact metric: graduates report a meaningful monthly income uplift within their first production season.</p>
  </div>
</section>
''' + cta_band(
    'Every product funds the <em>next artisan.</em>',
    "Shop the collection, or sponsor a full training batch, with sewing machines, trainers and materials included.",
    f'<a href="shop.html" class="btn btn-green btn-lg">Shop With Purpose {I["arrow"]}</a><a href="get-involved.html#partner" class="btn btn-outline-light btn-lg">Sponsor a Training Batch</a>'
)

# ================================================================ CSR
csr_body = page_hero(
    '<a href="initiatives.html">Our Initiatives</a><span class="sep">/</span><span>CSR Partnerships</span>',
    'Strategic CSR <span style="color:var(--green-deep)">partnerships.</span>',
    "Tailored solutions, measurable impact, and transparent reporting for corporate ESG goals.",
    f'<a href="resources.html" class="btn btn-green">Download CSR Deck {I["download"]}</a><a href="contact.html" class="btn btn-outline">Schedule Consultation</a>'
) + f'''
<section class="section" style="padding-top:40px">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Offerings</p>
      <h2>Waste programs your auditors will love.</h2>
    </div>
    <div class="feat-grid">
      {feat(I["recycle"], "bg-green-t", "Decentralised waste systems", "Campus-wide segregation infrastructure, operations, and digital tracking.")}
      {feat(I["heart"], "bg-terra-t", "Recovery &amp; empowerment", "Collection programs whose proceeds directly fund education and livelihoods.", "reveal-d1")}
      {feat(I["shield"], "bg-blue-t", "Transparent reporting", "Audit-ready documentation and official Zero Waste Green Certificates.", "reveal-d2")}
    </div>
  </div>
</section>

<section class="section" style="background:var(--cream-2)">
  <div class="wrap two-col">
    <div class="prose reveal">
      <p class="eyebrow">Volunteer engagement</p>
      <h3>Give your team a day they'll talk about.</h3>
      <p>CSR that employees actually feel: hands-on sessions at the hub, city-wide drives, and learning formats for every team size.</p>
      <ul class="check-list">
        <li><span><b>Kogilu Hub Experience:</b> sort, sanitise and pack alongside the team.</span></li>
        <li><span><b>Community collection drives:</b> company-branded neighbourhood drives.</span></li>
        <li><span><b>Masterclasses and Lunch-and-Learn:</b> on-site upcycling and circularity sessions.</span></li>
      </ul>
      <p style="margin-top:10px"><b>20 corporate-led volunteer programs</b> delivered so far, on the way to 60 by 2030.</p>
    </div>
    <div class="reveal reveal-d1">
      <div class="info-panel" style="position:static">
        <h3>The partnership flow</h3>
        <ul>
          <li>{I["check"]}<span><b>1. Baseline audit:</b> we map your waste streams and volumes</span></li>
          <li>{I["check"]}<span><b>2. Program design:</b> pick pillars that match your ESG goals</span></li>
          <li>{I["check"]}<span><b>3. Activation:</b> drives, volunteering and infrastructure roll-out</span></li>
          <li>{I["check"]}<span><b>4. Reporting:</b> quantified impact, certificates and 80G receipts</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>
''' + cta_band(
    "Let's design your <em>impact program.</em>",
    "One consultation is all it takes to scope a program that fits your campus, people, and reporting cycle.",
    f'<a href="contact.html" class="btn btn-green btn-lg">Schedule Consultation {I["arrow"]}</a><a href="resources.html" class="btn btn-outline-light btn-lg">Download CSR Deck</a>'
)

# ================================================================ SHOP
shop_body = page_hero(
    '<span>Shop With Purpose</span>',
    'Shop with <span style="color:var(--terra)">purpose.</span>',
    "Durable, stylish products made from reclaimed textiles. Every purchase funds a teacher. Handcrafted by EmpowHer artisans; 100% of proceeds fund LEACT's education programs.",
    f'<a href="#products" class="btn btn-green">Browse Products {I["arrow"]}</a><a href="#gifting" class="btn btn-outline">Corporate Gifting</a>'
) + f'''
<section class="section" id="products" style="padding-top:40px">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Categories</p>
      <h2>Made from reclaim, made to last.</h2>
      <p>Denim totes · backpacks · corporate organizers · gift bundles.</p>
    </div>
    <div class="prod-grid" data-render="products" data-variant="full"></div>
    <p style="margin-top:28px;font-size:.85rem;color:var(--ink-soft)">Every product page includes materials, care, lead time, and a one-sentence artisan story. Online checkout is coming soon. For now, orders are confirmed over email or phone.</p>
  </div>
</section>

<section class="section" id="gifting" style="background:var(--cream-2)">
  <div class="wrap two-col">
    <div class="prose reveal">
      <p class="eyebrow">Corporate gifting</p>
      <h3>Gifts that come with an impact report.</h3>
      <p>Custom bulk orders with your branding, artisan story cards, and full CSR documentation for tax and ESG reporting.</p>
      <ul class="check-list">
        <li><span><b>Custom branding:</b> logo embroidery and bespoke colourways.</span></li>
        <li><span><b>Bulk-ready:</b> production planning for 50 to 5,000 units.</span></li>
        <li><span><b>CSR reporting:</b> impact documentation with every order, 80G-eligible components.</span></li>
      </ul>
      <a href="contact.html" class="btn btn-terra" style="margin-top:12px">Request Bulk Quote {I["arrow"]}</a>
    </div>
    <div class="reveal reveal-d1">
      <div class="cta-band" style="text-align:left;padding:52px 44px">
        <h2 style="font-size:1.8rem">Every purchase <em>funds a teacher.</em></h2>
        <p style="margin:0 0 26px">20% of proceeds go directly to teacher salaries and school infrastructure through LEACT. The rest keeps artisans earning and the hub running.</p>
        <div class="hero-ctas" style="justify-content:flex-start">
          <a href="empowher.html" class="btn btn-outline-light">Meet the Artisans</a>
        </div>
      </div>
    </div>
  </div>
</section>
'''

# ================================================================ REQUEST PICKUP
pickup_body = page_hero(
    '<span>Request a Pick-Up</span>',
    'Request a <span style="color:var(--green-deep)">pick-up.</span>',
    "Schedule a contactless collection. We will sort, sanitise and divert your items to reuse or upcycling, free across Bengaluru."
) + f'''
<section class="section" style="padding-top:30px">
  <div class="wrap two-col form-layout">
    <div class="form-card reveal">
      <h3 style="font-size:1.5rem;margin-bottom:26px">Schedule your collection</h3>
      <form action="https://formsubmit.co/reclaimera@gmail.com" method="POST">
        <input type="hidden" name="_subject" value="New pick-up request (reclaimera.in)"><input type="hidden" name="form_type" value="Pick-up request"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_template" value="table"><input type="text" name="_honey" style="display:none" tabindex="-1" aria-hidden="true">
        <div class="form-grid">
          <div class="field"><label for="p-name">Full name <span>*</span></label><input id="p-name" name="name" type="text" placeholder="Your name" required></div>
          <div class="field"><label for="p-phone">Phone <span>*</span></label><input id="p-phone" name="phone" type="tel" placeholder="+91" required></div>
          <div class="field full"><label for="p-email">Email</label><input id="p-email" name="email" type="email" placeholder="you@example.com"></div>
          <div class="field full"><label for="p-addr">Pickup address <span>*</span></label><textarea id="p-addr" name="address" placeholder="Flat / street / area / PIN" required></textarea></div>
          <div class="field"><label for="p-date">Preferred date <span>*</span></label><input id="p-date" name="preferred_date" type="date" required></div>
          <div class="field"><label for="p-time">Preferred time</label>
            <select id="p-time" name="preferred_time"><option>Morning (9–12)</option><option>Afternoon (12–4)</option><option>Evening (4–7)</option></select>
          </div>
          <div class="field"><label for="p-items">Item types <span>*</span></label>
            <select id="p-items" name="item_types" required><option value="">Select…</option><option>Clothes &amp; textiles</option><option>Household items</option><option>Books &amp; stationery</option><option>Mixed</option></select>
          </div>
          <div class="field"><label for="p-qty">Approx. quantity</label>
            <select id="p-qty" name="quantity"><option>1–2 bags</option><option>3–5 bags</option><option>6–10 bags</option><option>Bulk / society drive</option></select>
          </div>
          <div class="field full checkbox-row"><input id="p-receipt" name="donation_receipt" value="Yes" type="checkbox"><label for="p-receipt" style="margin:0;font-weight:500">Send me a donation receipt (12A &amp; 80G eligible)</label></div>
        </div>
        <button class="btn btn-green btn-lg" type="submit" style="margin-top:26px;width:100%">Schedule Pickup {I["arrow"]}</button>
        <div class="form-success" role="status">{I["check"]}<span>Thank you! Your pick-up request is in. Our team will confirm your slot within 24 hours.</span></div>
        <div class="form-error" role="alert"><span data-msg>Could not send right now. Please try again, or email reclaimera@gmail.com directly.</span></div>
      </form>
    </div>
    <div>
      <div class="info-panel reveal reveal-d1">
        <h3>Good to know</h3>
        <ul>
          <li>{I["check"]}<span><b>Areas covered:</b> all of Bengaluru, from Yelahanka to Electronic City</span></li>
          <li>{I["check"]}<span><b>Turnaround:</b> slot confirmed within 24 hours; pick-up usually within 3–5 days</span></li>
          <li>{I["check"]}<span><b>We accept:</b> clothes, textiles, household items, toys, books &amp; stationery</span></li>
          <li>{I["check"]}<span><b>Contactless:</b> leave labelled bags at your door and we handle the rest</span></li>
          <li>{I["check"]}<span><b>Receipts:</b> donation receipts eligible under sections 12A &amp; 80G</span></li>
        </ul>
        <div class="contact-line">{I["phone"]}<a href="tel:+918152020145" data-phone>+91 81520 20145</a></div>
        <div class="contact-line">{I["mail"]}<a href="mailto:reclaimera@gmail.com">reclaimera@gmail.com</a></div>
      </div>
    </div>
  </div>
</section>
'''

# ================================================================ ZERO WASTE
zero_body = page_hero(
    '<span>Zero Waste Certification &amp; AMC</span>',
    'Achieve zero waste <span style="color:var(--green-deep)">compliance.</span>',
    "A full AMC covering infrastructure, operations, digital tracking and resident education to meet SWM 2026 mandates, with official Zero Waste Green Certificates.",
    f'<a href="contact.html" class="btn btn-green">Book Free Campus Audit {I["arrow"]}</a><a href="contact.html" class="btn btn-outline">Request AMC Pricing</a>'
) + f'''
<section class="section" style="padding-top:40px;padding-bottom:60px">
  <div class="wrap two-col">
    <div class="prose reveal">
      <p class="eyebrow">The SWM 2026 mandate</p>
      <h3>Bulk Waste Generators, the clock is ticking.</h3>
      <p>Under SWM 2026, Bulk Waste Generators (BWGs), which include apartments, campuses and offices, must implement <b>source segregation</b> and maintain <b>digital records</b> of their waste streams.</p>
      <p>Reclaim Era provides turnkey compliance: we design, build, operate, and document your entire waste system, so audits become a formality instead of a fire drill.</p>
    </div>
    <div class="reveal reveal-d1">
      <div class="info-panel" style="position:static">
        <h3>What certification gets you</h3>
        <ul>
          <li>{I["check"]}<span>Official <b>Zero Waste Green Certificate</b> for BWG compliance</span></li>
          <li>{I["check"]}<span>Audit-ready daily logs and weighbridge documentation</span></li>
          <li>{I["check"]}<span>BWG registration support with authorities</span></li>
          <li>{I["check"]}<span>Quarterly audits and resident engagement reports</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--cream-2)">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">4-phase implementation</p>
      <h2>From baseline to certified, step by step.</h2>
    </div>
    <div class="phase-grid">
      <div class="phase reveal"><span class="ph-num">1</span><div><h4>Physical infrastructure</h4><p>A four-bin system, a dedicated waste room and clear signage across the campus.</p></div></div>
      <div class="phase reveal reveal-d1"><span class="ph-num">2</span><div><h4>Operations</h4><p>Collection schedules and secondary segregation checks, run like clockwork.</p></div></div>
      <div class="phase reveal reveal-d2"><span class="ph-num">3</span><div><h4>Digital tracking</h4><p>Daily logs, weighbridge slips and BWG registration support, all audit-ready.</p></div></div>
      <div class="phase reveal reveal-d3"><span class="ph-num">4</span><div><h4>Resident education</h4><p>Induction kits, quarterly audits, and resident waste committees that stick.</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Segregation protocol</p>
      <h2>Four bins. Zero confusion.</h2>
    </div>
    <div class="bin-grid">
      <div class="bin green reveal"><div class="bin-dot">{I["leaf"]}</div><h4>Green Bin</h4><span class="cat">Wet · Biodegradable</span><p>Food scraps and garden waste, composted instead of dumped.</p></div>
      <div class="bin blue reveal reveal-d1"><div class="bin-dot">{I["recycle"]}</div><h4>Blue Bin</h4><span class="cat">Dry · Recyclable</span><p>Paper, plastics and glass, routed to recyclers.</p></div>
      <div class="bin red reveal reveal-d2"><div class="bin-dot">{I["warn"]}</div><h4>Red Bin</h4><span class="cat">Domestic Hazardous</span><p>Batteries, bulbs and e-waste, handled by authorised processors.</p></div>
      <div class="bin black reveal reveal-d3"><div class="bin-dot">{I["trash"]}</div><h4>Black Bin</h4><span class="cat">Reject · Other</span><p>Sanitary waste and contaminated plastics, minimised over time.</p></div>
    </div>
  </div>
</section>
''' + cta_band(
    'Get compliant before the <em>deadline does.</em>',
    "Start with a free campus audit. We will map your waste streams and hand you a compliance roadmap the same week.",
    f'<a href="contact.html" class="btn btn-green btn-lg">Book Free Campus Audit {I["arrow"]}</a><a href="contact.html" class="btn btn-outline-light btn-lg">Request AMC Pricing</a>'
)

# ================================================================ GET INVOLVED
involved_body = page_hero(
    '<span>Get Involved</span>',
    "Let's join <span style=\"color:var(--terra)\">hands.</span>",
    "Volunteer, partner or donate. Every action helps build a landfill-free Bengaluru and supports children's education."
) + f'''
<section class="section" style="padding-top:30px">
  <div class="wrap">
    <div class="init-grid">
      <div class="init-card t-green reveal" id="host-campaign" style="border:2px solid var(--green)">
        <div class="icon-chip bg-green-t">{I["truck"]}</div>
        <span class="metric">Bring us to you</span>
        <h3>Host a Campaign</h3>
        <p>Run a used-clothes collection drive at your apartment complex, company, campus or store. We bring the crew, bins and vehicle; a one-time \u20B9500 logistics fee confirms your slot.</p>
        <a href="campaign-application.html" class="btn btn-green" style="margin-top:auto;align-self:flex-start">Apply to Host {I["arrow"]}</a>
      </div>
      <div class="init-card t-blue reveal reveal-d1" id="volunteer">
        <div class="icon-chip bg-blue-t">{I["users"]}</div>
        <span class="metric">Weekends · Kogilu hub</span>
        <h3>Volunteer</h3>
        <p>Join the Sorting Squad, run weekend collection drives, or host an upcycling masterclass at the hub.</p>
        <a href="contact.html" class="btn btn-green" style="margin-top:auto;align-self:flex-start">Volunteer Now {I["arrow"]}</a>
      </div>
      <div class="init-card t-gold reveal reveal-d2" id="partner">
        <div class="icon-chip bg-gold-t">{I["handshake"]}</div>
        <span class="metric">For companies</span>
        <h3>Partner (CSR)</h3>
        <p>Sponsor EmpowHer training batches, host collection drives, or place bulk gifting orders with full impact reporting.</p>
        <a href="csr-partnerships.html" class="btn btn-ink" style="margin-top:auto;align-self:flex-start">Partner With Us {I["arrow"]}</a>
      </div>
      <div class="init-card t-terra reveal reveal-d3" id="donate">
        <div class="icon-chip bg-terra-t">{I["heart"]}</div>
        <span class="metric">12A &amp; 80G tax-exempt</span>
        <h3>Donate</h3>
        <p>One-time or monthly giving that funds teacher salaries, notebooks and school infrastructure through LEACT.</p>
        <a href="contact.html" class="btn btn-terra" style="margin-top:auto;align-self:flex-start">Donate Now {I["arrow"]}</a>
      </div>
      <div class="init-card t-green reveal" id="donate-equipment">
        <div class="icon-chip bg-green-t">{I["laptop"]}</div>
        <span class="metric">Hardware with a second life</span>
        <h3>Donate Equipment</h3>
        <p>Working laptops, sewing machines, and tablets power the EmpowHer academy and school programs.</p>
        <a href="contact.html" class="btn btn-ink" style="margin-top:auto;align-self:flex-start">Donate Tech {I["arrow"]}</a>
      </div>
    </div>
  </div>
</section>
''' + cta_band(
    'Not sure which way to <em>help?</em>',
    "Send us a note and we will match your time, skills or budget to the program that needs it most this month.",
    f'<a href="contact.html" class="btn btn-green btn-lg">Talk to Us {I["arrow"]}</a><a href="campaign-application.html" class="btn btn-outline-light btn-lg">Host a Campaign</a>'
)

# ================================================================ RESOURCES
resources_body = page_hero(
    '<span>Resources</span>',
    '<span style="color:var(--green-deep)">Resources</span> &amp; reports.',
    "Guides, reports, and stories to help you run zero-waste drives and support circular livelihoods."
) + f'''
<section class="section" style="padding-top:30px">
  <div class="wrap">
    <div class="res-grid">
      <a href="#" class="res-card reveal"><div class="icon-chip bg-green-t">{I["book"]}</div><div><h4>Blog</h4><p>How-to guides, upcycling tutorials, and classroom activity ideas.</p><span class="text-link">Read articles {I["arrow"]}</span></div></a>
      <a href="#" class="res-card reveal reveal-d1"><div class="icon-chip bg-blue-t">{I["file"]}</div><div><h4>Reports &amp; Impact</h4><p>The annual impact report: items diverted, livelihoods created and rupees routed to education.</p><span class="text-link">Download report {I["arrow"]}</span></div></a>
      <a href="#" class="res-card reveal reveal-d2"><div class="icon-chip bg-terra-t">{I["spark"]}</div><div><h4>Case Studies</h4><p>Corporate audits, school partnerships, and EmpowHer success stories in detail.</p><span class="text-link">Browse case studies {I["arrow"]}</span></div></a>
      <a href="#" class="res-card reveal reveal-d3"><div class="icon-chip bg-gold-t">{I["camera"]}</div><div><h4>Media Kit &amp; Press</h4><p>Logos, photography, boilerplate, and press releases for journalists and partners.</p><span class="text-link">Get the kit {I["arrow"]}</span></div></a>
    </div>
  </div>
</section>

<section class="section" style="background:var(--cream-2)">
  <div class="wrap" style="max-width:860px">
    <div class="section-head center">
      <p class="eyebrow">FAQs</p>
      <h2>Questions, answered.</h2>
    </div>
    <div class="accordion">
      <div class="acc-item"><button class="acc-btn" aria-expanded="false">What items do you accept for pick-up?<span class="plus">+</span></button><div class="acc-body"><p>Clothes and textiles in any condition, household items, toys, books, and stationery. Wearables are sanitised and donated; the rest is upcycled or recycled. Nothing goes to landfill.</p></div></div>
      <div class="acc-item"><button class="acc-btn" aria-expanded="false">Is the pick-up really free?<span class="plus">+</span></button><div class="acc-body"><p>Yes. Household pick-ups across Bengaluru are free. For bulk or society-wide drives we'll coordinate logistics with your RWA at no cost to residents.</p></div></div>
      <div class="acc-item"><button class="acc-btn" aria-expanded="false">Are donations tax-exempt?<span class="plus">+</span></button><div class="acc-body"><p>Yes. Reclaim Era operates under Lamp Educational and Charitable Trust (LEACT); monetary donations are eligible under sections 12A &amp; 80G, and we issue receipts on request.</p></div></div>
      <div class="acc-item"><button class="acc-btn" aria-expanded="false">Where do the shop proceeds go?<span class="plus">+</span></button><div class="acc-body"><p>Proceeds keep EmpowHer artisans earning and fund LEACT's education programs, including teacher salaries and school infrastructure. 20% of proceeds go there directly.</p></div></div>
      <div class="acc-item"><button class="acc-btn" aria-expanded="false">How does Zero Waste Certification work?<span class="plus">+</span></button><div class="acc-body"><p>We run a four-phase program covering infrastructure, operations, digital tracking and resident education. After it, your campus receives an official Zero Waste Green Certificate and audit-ready documentation for SWM 2026 compliance.</p></div></div>
    </div>
  </div>
</section>
''' + cta_band(
    'Stay in the <em>loop.</em>',
    "Get the latest report the day it drops, plus monthly events and volunteering invites.",
    f'<a href="#" class="btn btn-green btn-lg">Read the Latest Report {I["arrow"]}</a><a href="contact.html" class="btn btn-outline-light btn-lg">Subscribe for Updates</a>'
)

# ================================================================ CONTACT
contact_body = page_hero(
    '<span>Contact</span>',
    'Contact <span style="color:var(--green-deep)">us.</span>',
    "We are here to help with pickups, partnerships, volunteering and media requests."
) + f'''
<section class="section" style="padding-top:30px">
  <div class="wrap two-col form-layout">
    <div class="form-card reveal">
      <h3 style="font-size:1.5rem;margin-bottom:26px">Send us a message</h3>
      <form action="https://formsubmit.co/reclaimera@gmail.com" method="POST">
        <input type="hidden" name="_subject" value="New contact inquiry (reclaimera.in)"><input type="hidden" name="form_type" value="Contact form"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_template" value="table"><input type="text" name="_honey" style="display:none" tabindex="-1" aria-hidden="true">
        <div class="form-grid">
          <div class="field"><label for="c-name">Name <span>*</span></label><input id="c-name" name="name" type="text" placeholder="Your name" required></div>
          <div class="field"><label for="c-company">Company (optional)</label><input id="c-company" name="company" type="text" placeholder="Organisation"></div>
          <div class="field"><label for="c-email">Email <span>*</span></label><input id="c-email" name="email" type="email" placeholder="you@example.com" required></div>
          <div class="field"><label for="c-phone">Phone</label><input id="c-phone" name="phone" type="tel" placeholder="+91"></div>
          <div class="field full"><label for="c-interest">Area of interest <span>*</span></label>
            <select id="c-interest" name="area_of_interest" required><option value="">Select…</option><option>Request a Pick-Up</option><option>CSR Partnership</option><option>Zero Waste Certification / AMC</option><option>School Program (NEP 2020)</option><option>Volunteering</option><option>Donation</option><option>Shop / Bulk Orders</option><option>Media</option></select>
          </div>
          <div class="field full"><label for="c-msg">Message <span>*</span></label><textarea id="c-msg" name="message" placeholder="Tell us a little about what you need…" required></textarea></div>
        </div>
        <button class="btn btn-green btn-lg" type="submit" style="margin-top:26px;width:100%">Submit Inquiry {I["arrow"]}</button>
        <div class="form-success" role="status">{I["check"]}<span>Message received! We usually reply within one working day.</span></div>
        <div class="form-error" role="alert"><span data-msg>Could not send right now. Please try again, or email reclaimera@gmail.com directly.</span></div>
      </form>
    </div>
    <div>
      <div class="info-panel reveal reveal-d1">
        <h3>Direct lines</h3>
        <ul>
          <li>{I["pin"]}<span><b>Kogilu Hub</b><br>Yelahanka, Bengaluru, Karnataka</span></li>
          <li>{I["mail"]}<span><b>CSR &amp; partnerships</b><br>Smitha Rajarathinam<br><a href="mailto:reclaimera@gmail.com" style="text-decoration:underline">reclaimera@gmail.com</a></span></li>
          <li>{I["phone"]}<span><b>Phone</b><br><span data-phone>+91 81520 20145</span><br>+91 74830 42681</span></li>
          <li>{I["cal"]}<span><b>Hub visits</b><br>Weekdays 10:00–17:00, by appointment</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>
'''



# ================================================================ LEGAL + 404
def legal_section(title, body):
    return f'<h3 style="font-size:1.25rem;margin:30px 0 10px">{title}</h3><p style="color:var(--ink-soft)">{body}</p>'

privacy_body = page_hero('<span>Privacy Policy</span>', 'Privacy <span style="color:var(--green-deep)">policy.</span>',
    'How Reclaim Era (Lamp Educational and Charitable Trust) collects, uses and protects your information.') + '''
<section class="section" style="padding-top:10px"><div class="wrap" style="max-width:820px"><div class="prose">''' + \
legal_section('What we collect', 'When you use our forms we collect the details you type in: your name, phone number, email address, pickup or campaign address, and your message. When you pay the campaign logistics fee, the payment is processed by Razorpay; we receive a payment reference and status, and we never see or store your card, UPI or bank details.') + \
legal_section('How we use it', 'We use your details only to run our services: scheduling pickups, coordinating campaigns, responding to enquiries, issuing receipts, and sending updates you have asked for. We do not sell or rent your information to anyone.') + \
legal_section('Where it goes', 'Form submissions are delivered to our team by email. Campaign applications and their payment status are stored in our secure database. Payments are handled by Razorpay under their own privacy policy. We share information with no other third parties unless the law requires it.') + \
legal_section('Cookies and tracking', 'This site does not use advertising cookies. Local storage in your browser is used only for site functionality.') + \
legal_section('Your rights', 'You can ask us at any time to see, correct or delete the information we hold about you. Write to reclaimera@gmail.com and we will respond within a reasonable time.') + \
legal_section('Contact', 'Reclaim Era, an initiative of Lamp Educational and Charitable Trust (LEACT), Kogilu, Yelahanka, Bengaluru, Karnataka. Email: reclaimera@gmail.com. Phone: +91 81520 20145.') + \
'</div></div></section>'

terms_body = page_hero('<span>Terms &amp; Conditions</span>', 'Terms &amp; <span style="color:var(--green-deep)">conditions.</span>',
    'The terms that apply when you use this website and our services.') + '''
<section class="section" style="padding-top:10px"><div class="wrap" style="max-width:820px"><div class="prose">''' + \
legal_section('Who we are', 'This website is operated by Reclaim Era, an initiative of Lamp Educational and Charitable Trust (LEACT), Bengaluru, Karnataka, India.') + \
legal_section('Using this site', 'You agree to use this site lawfully and to provide accurate information in our forms. We may update content, services and these terms from time to time; the version published here applies.') + \
legal_section('Pickups and campaigns', 'Pickup requests and campaign applications are requests for service and are confirmed by our team over phone or email. The campaign logistics fee of \u20B9500 covers the collection vehicle, crew and materials for a scheduled campaign; it is a service fee and not a donation. Scheduling is subject to our team\u2019s availability and service area.') + \
legal_section('Payments', 'Online payments are processed by Razorpay. By paying you agree to Razorpay\u2019s terms. Refunds are governed by our Refund &amp; Cancellation Policy.') + \
legal_section('Donations', 'Monetary donations to LEACT are eligible for exemption under sections 12A and 80G of the Income Tax Act; receipts are issued on request. Donated goods are sorted at our discretion into reuse, upcycling or recycling.') + \
legal_section('Content and branding', 'The Reclaim Era name, logo and site content belong to LEACT and may not be reproduced without permission, except for fair, non-commercial reference.') + \
legal_section('Liability', 'We provide this site and our services with care but without warranties. To the extent permitted by law, LEACT is not liable for indirect or consequential losses arising from use of the site.') + \
legal_section('Governing law', 'These terms are governed by the laws of India, with courts in Bengaluru, Karnataka having jurisdiction.') + \
legal_section('Contact', 'Questions about these terms: reclaimera@gmail.com \u00B7 +91 81520 20145.') + \
'</div></div></section>'

refund_body = page_hero('<span>Refund &amp; Cancellation Policy</span>', 'Refund &amp; cancellation <span style="color:var(--green-deep)">policy.</span>',
    'How refunds work for the \u20B9500 campaign logistics fee.') + '''
<section class="section" style="padding-top:10px"><div class="wrap" style="max-width:820px"><div class="prose">''' + \
legal_section('The logistics fee', 'The \u20B9500 fee paid with a campaign application covers the collection vehicle, crew and materials for your scheduled campaign day. It is a service fee, not a donation.') + \
legal_section('If you cancel', 'Cancel at least 48 hours before your scheduled campaign date and we will refund the fee in full. Cancellations within 48 hours of the scheduled date are not refundable, because the vehicle and crew are already committed.') + \
legal_section('If we cancel or cannot serve you', 'If we cannot schedule your campaign (for example, your location is outside our service area) or we cancel for any reason, you receive a full refund automatically.') + \
legal_section('How refunds are paid', 'Refunds are issued to your original payment method through Razorpay, normally within 5\u20137 business days of the refund being initiated.') + \
legal_section('How to request one', 'Email reclaimera@gmail.com or call +91 81520 20145 with your payment reference (shown on your success screen and Razorpay receipt).') + \
'</div></div></section>'

notfound_body = '''
<section class="section" style="text-align:center;padding-top:90px">
  <div class="wrap" style="max-width:560px">
    <p style="font-family:var(--font-display);font-weight:800;font-size:5rem;line-height:1;color:var(--green)">404</p>
    <h1 style="font-size:2rem;margin:14px 0 12px">This page took the recycling route.</h1>
    <p style="color:var(--ink-soft);margin-bottom:28px">The link you followed does not exist any more. Everything useful is one tap away:</p>
    <div class="hero-ctas" style="justify-content:center">
      <a href="index.html" class="btn btn-green">Go to the Home page</a>
      <a href="request-pickup.html" class="btn btn-outline">Request a Pick-Up</a>
    </div>
  </div>
</section>'''

# ================================================================ CAMPAIGN APPLICATION
CAMPAIGN_JS = r"""
<script>
(function () {
  "use strict";

  /* CHANGE ME after deploying the backend (see backend/README.md) */
  var API_BASE = (location.hostname === "localhost" || location.hostname === "127.0.0.1")
    ? "http://localhost:5001"
    : "https://REPLACE-WITH-DEPLOYED-BACKEND";

  var form = document.getElementById("campaignForm");
  if (!form) return;

  var state = {};

  function q(id) { return document.getElementById(id); }
  function esc(t) {
    return String(t == null ? "" : t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function setStep(n) {
    form.querySelectorAll(".form-step").forEach(function (el) {
      el.classList.toggle("active", el.getAttribute("data-step") == n);
    });
    document.querySelectorAll(".step-pill").forEach(function (el) {
      var k = parseInt(el.getAttribute("data-pill"), 10);
      el.classList.toggle("active", k === n);
      el.classList.toggle("done", k < n);
    });
    hideError();
    form.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function markInvalid(id, bad) {
    q(id).closest(".field").classList.toggle("invalid", bad);
  }

  var PHONE_RE = /^(\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}$/;
  var EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  var UTR_RE = /^[A-Za-z0-9]{10,23}$/;

  q("cf-type").addEventListener("change", function () {
    document.getElementById("otherWrap").style.display = this.value === "Other" ? "" : "none";
  });

  function validateStep1() {
    var ok = true;
    state.location_type = q("cf-type").value;
    state.location_other = q("cf-other").value.trim();
    state.institution_name = q("cf-name").value.trim();
    state.address = q("cf-address").value.trim();
    markInvalid("cf-type", !state.location_type); ok = ok && !!state.location_type;
    var needOther = state.location_type === "Other";
    markInvalid("cf-other", needOther && state.location_other.length < 2);
    ok = ok && (!needOther || state.location_other.length >= 2);
    markInvalid("cf-name", state.institution_name.length < 2); ok = ok && state.institution_name.length >= 2;
    markInvalid("cf-address", state.address.length < 10); ok = ok && state.address.length >= 10;
    return ok;
  }

  function validateStep2() {
    var ok = true;
    state.contact_name = q("cf-contact").value.trim();
    state.contact_phone = q("cf-phone").value.trim();
    state.contact_email = q("cf-email").value.trim();
    markInvalid("cf-contact", state.contact_name.length < 2); ok = ok && state.contact_name.length >= 2;
    markInvalid("cf-phone", !PHONE_RE.test(state.contact_phone)); ok = ok && PHONE_RE.test(state.contact_phone);
    markInvalid("cf-email", !EMAIL_RE.test(state.contact_email)); ok = ok && EMAIL_RE.test(state.contact_email);
    return ok;
  }

  function buildReview() {
    q("reviewDl").innerHTML =
      "<dt>Location type</dt><dd>" + esc(state.location_type + (state.location_other ? " - " + state.location_other : "")) + "</dd>" +
      "<dt>Institution</dt><dd>" + esc(state.institution_name) + "</dd>" +
      "<dt>Address</dt><dd>" + esc(state.address) + "</dd>" +
      "<dt>Coordinator</dt><dd>" + esc(state.contact_name) + "</dd>" +
      "<dt>Phone</dt><dd>" + esc(state.contact_phone) + "</dd>" +
      "<dt>Email</dt><dd>" + esc(state.contact_email) + "</dd>";
  }

  q("next1").addEventListener("click", function () { if (validateStep1()) setStep(2); });
  q("back2").addEventListener("click", function () { setStep(1); });
  q("next2").addEventListener("click", function () { if (validateStep2()) { buildReview(); setStep(3); } });
  q("back3").addEventListener("click", function () { setStep(2); });

  q("copyUpi").addEventListener("click", function () {
    navigator.clipboard.writeText("lampeducational@ybl").then(function () {
      q("copyUpi").textContent = "Copied!";
      setTimeout(function () { q("copyUpi").textContent = "Copy"; }, 1600);
    });
  });

  var payBtn = q("paySubmit");
  function setBusy(b) {
    payBtn.disabled = b;
    payBtn.textContent = b ? "Submitting\u2026" : "Submit Application";
  }
  function showError(msg) {
    var box = q("campaignError");
    box.querySelector("[data-msg]").textContent = msg;
    box.classList.add("show");
  }
  function hideError() { q("campaignError").classList.remove("show"); }

  function showSuccess(refId) {
    form.style.display = "none";
    document.querySelector(".steps-nav").style.display = "none";
    q("successRef").textContent = "Application reference: " + refId;
    q("successPanel").style.display = "block";
    q("successPanel").scrollIntoView({ behavior: "smooth", block: "center" });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    hideError();
    if (!validateStep1() || !validateStep2()) { setStep(!validateStep1() ? 1 : 2); return; }
    state.upi_utr = q("cf-utr").value.trim();
    var utrOk = UTR_RE.test(state.upi_utr);
    markInvalid("cf-utr", !utrOk);
    if (!utrOk) return;
    setBusy(true);

    fetch(API_BASE + "/api/campaign/submit-upi", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state)
    })
      .then(function (res) { return res.json().then(function (d) { return { ok: res.ok, d: d }; }); })
      .then(function (r) {
        if (!r.ok || !r.d.ok) {
          var msgs = r.d && r.d.errors ? Object.values(r.d.errors).join(" ") : (r.d && r.d.error);
          throw new Error(msgs || "Could not submit the application. Please try again.");
        }
        showSuccess(r.d.application_id);
      })
      .catch(function (err) {
        setBusy(false);
        var m = err && err.message ? err.message : "";
        if (!m || /fetch|network|load failed/i.test(m)) {
          m = "Could not reach our server right now. Please try again in a minute, or email reclaimera@gmail.com \u2014 your payment is safe.";
        }
        showError(m);
      });
  });
})();
</script>
"""

campaign_body = page_hero(
    '<span>Host a Campaign</span>',
    'Donation campaign <span style="color:var(--green-deep)">application.</span>',
    "Bring a Reclaim Era used-clothes collection drive to your apartment complex, company, campus, store or restaurant. A one-time \u20B9500 logistics fee, paid by UPI, confirms your slot and covers the collection vehicle and crew."
) + f'''
<section class="section" style="padding-top:30px">
  <div class="wrap two-col form-layout">
    <div>
      <div class="steps-nav" aria-hidden="true">
        <div class="step-pill active" data-pill="1"><span class="num">1</span><span class="lbl">Location</span></div>
        <div class="step-pill" data-pill="2"><span class="num">2</span><span class="lbl">Contact</span></div>
        <div class="step-pill" data-pill="3"><span class="num">3</span><span class="lbl">Review &amp; Pay</span></div>
      </div>
      <div class="form-card">
        <form id="campaignForm" novalidate>
          <div class="form-step active" data-step="1">
            <h3 style="font-size:1.4rem;margin-bottom:22px">Where will the campaign run?</h3>
            <div class="form-grid">
              <div class="field full"><label for="cf-type">Type of location <span>*</span></label>
                <select id="cf-type" required><option value="">Select\u2026</option><option>Apartment Complex</option><option>Companies</option><option>School</option><option>College/University</option><option>Small/Medium Business (SMB)</option><option>Restaurants/GYM/Hotels/Super Markets/Malls</option><option>Other</option></select>
                <p class="field-error">Choose the type of location.</p>
              </div>
              <div class="field full" id="otherWrap" style="display:none"><label for="cf-other">Please specify the location type <span>*</span></label>
                <input id="cf-other" type="text" placeholder="Tell us what kind of place it is">
                <p class="field-error">Tell us what kind of location this is.</p>
              </div>
              <div class="field full"><label for="cf-name">Name of the institution / apartment complex <span>*</span></label>
                <input id="cf-name" type="text" placeholder="e.g. Green Meadows Apartments" required>
                <p class="field-error">Enter the name of the institution or apartment complex.</p>
              </div>
              <div class="field full"><label for="cf-address">Complete address for the campaign <span>*</span></label>
                <textarea id="cf-address" placeholder="Building / street / area / city / PIN" required></textarea>
                <p class="field-error">Enter the complete address, including area and PIN code.</p>
              </div>
            </div>
            <div class="step-actions"><span></span><button type="button" class="btn btn-green" id="next1">Next: Contact details {I["arrow"]}</button></div>
          </div>

          <div class="form-step" data-step="2">
            <h3 style="font-size:1.4rem;margin-bottom:22px">Who should we coordinate with?</h3>
            <div class="form-grid">
              <div class="field full"><label for="cf-contact">Coordinator / contact person name <span>*</span></label>
                <input id="cf-contact" type="text" placeholder="Full name" required>
                <p class="field-error">Enter the coordinator or contact person's name.</p>
              </div>
              <div class="field"><label for="cf-phone">Contact phone number <span>*</span></label>
                <input id="cf-phone" type="tel" placeholder="+91 98765 43210" required>
                <p class="field-error">Enter a valid Indian mobile number.</p>
              </div>
              <div class="field"><label for="cf-email">Contact email <span>*</span></label>
                <input id="cf-email" type="email" placeholder="you@example.com" required>
                <p class="field-error">Enter a valid email address.</p>
              </div>
            </div>
            <div class="step-actions">
              <button type="button" class="btn btn-outline" id="back2">Back</button>
              <button type="button" class="btn btn-green" id="next2">Review application {I["arrow"]}</button>
            </div>
          </div>

          <div class="form-step" data-step="3">
            <h3 style="font-size:1.4rem;margin-bottom:22px">Review &amp; pay by UPI</h3>
            <div class="review-list"><dl id="reviewDl"></dl></div>
            <div class="fee-row"><span>Logistics fee</span><span class="amt">\u20B9500</span></div>
            <div class="upi-box">
              <div class="upi-qr"><img src="assets/upi-qr.png" alt="UPI QR code to pay \u20B9500 to lampeducational@ybl" loading="lazy"></div>
              <div class="upi-info">
                <p class="upi-title">Pay \u20B9500 with any UPI app</p>
                <p>Scan the QR with GPay, PhonePe or Paytm. On your phone, just tap the button below.</p>
                <a class="btn btn-green upi-open" href="upi://pay?pa=lampeducational@ybl&amp;pn=LAMP%20Educational%20Trust&amp;am=500&amp;cu=INR&amp;tn=Reclaim%20Era%20campaign%20fee">Open UPI app &amp; pay \u20B9500</a>
                <div class="upi-id-row"><span>UPI ID: <b>lampeducational@ybl</b></span><button type="button" class="btn btn-outline btn-sm" id="copyUpi">Copy</button></div>
              </div>
            </div>
            <div class="form-grid" style="margin-top:16px">
              <div class="field full"><label for="cf-utr">UPI transaction / reference number (UTR) <span>*</span></label>
                <input id="cf-utr" type="text" placeholder="e.g. 415912345678" autocomplete="off">
                <p class="field-error">Enter the reference / UTR number from your UPI app.</p>
                <p class="hint">After paying, open the transaction in your UPI app \u2014 the 12-digit UTR / reference number is shown in its details.</p>
              </div>
            </div>
            <div class="step-actions">
              <button type="button" class="btn btn-outline" id="back3">Back</button>
              <button type="submit" class="btn btn-green btn-lg" id="paySubmit">Submit Application</button>
            </div>
          </div>

          <div class="form-error" id="campaignError" role="alert"><span data-msg></span></div>
        </form>

        <div class="success-panel" id="successPanel" style="display:none">
          <div class="big-tick">{I["check"]}</div>
          <h3>Application received!</h3>
          <p>Our team will verify your \u20B9500 UPI payment and call your coordinator within 48 hours to fix the campaign date.</p>
          <p>Keep your UPI reference handy in case we need to match the payment.</p>
          <span class="ref" id="successRef"></span>
        </div>
      </div>
    </div>
    <div>
      <div class="info-panel reveal reveal-d1">
        <h3>What happens next</h3>
        <ul>
          <li>{I["check"]}<span><b>Within 48 hours:</b> we confirm your campaign date over a call</span></li>
          <li>{I["check"]}<span><b>Before the day:</b> posters and a Revive Station are set up at your location</span></li>
          <li>{I["check"]}<span><b>Campaign day:</b> our crew collects, sorts and weighs everything on site</span></li>
          <li>{I["check"]}<span><b>After:</b> you receive an impact summary of items diverted and donated</span></li>
        </ul>
        <div class="contact-line">{I["mail"]}<a href="mailto:reclaimera@gmail.com">reclaimera@gmail.com</a></div>
        <div class="contact-line">{I["phone"]}<a href="tel:+918152020145" data-phone>+91 81520 20145</a></div>
      </div>
    </div>
  </div>
</section>
''' + CAMPAIGN_JS

# ================================================================ write files
PAGES = {
"index.html": ("Reclaim Era — Waste to Wisdom | Upcycle, Educate, Empower Bengaluru",
    "Reclaim Era turns Bengaluru's textile waste into education and dignified livelihoods. Request a pickup, partner for CSR, or shop upcycled products.",
    "", home_body, HOME_LD),
"about.html": ("About Reclaim Era — Mission, Story & Team",
    "Learn how Reclaim Era began, our dual-impact model, and the team turning textile waste into education and livelihoods in Bengaluru.",
    "about", about_body, ""),
"initiatives.html": ("Our Initiatives — Waste Management, Education, EmpowHer, CSR",
    "Explore Reclaim Era's four pillars: Waste Management, CSR Partnerships, Environmental Education (NEP 2020), and EmpowHer women's upskilling.",
    "initiatives", initiatives_body, ""),
"waste-management.html": ("Textile Waste Management & Recovery Factory | Reclaim Era",
    "End-to-end textile recovery at the Kogilu hub: sorting, upcycling, and downcycling to ensure zero landfill and measurable impact.",
    "initiatives", waste_body, ""),
"education.html": ("Environmental Education for Schools | NEP 2020 Aligned Programs",
    "A 1-year hands-on environmental curriculum aligned to NEP 2020 and NCF 2023: workshops, student-led audits, and on-campus Revive Stations.",
    "initiatives", education_body, ""),
"empowher.html": ("EmpowHer — Women's Upcycling Academy | Reclaim Era",
    "EmpowHer trains women in tailoring, digital literacy, and ecommerce to create premium upcycled products and stable livelihoods.",
    "initiatives", empowher_body, ""),
"csr-partnerships.html": ("CSR Partnerships & Corporate Waste Audits | Reclaim Era",
    "Tailored CSR programs that convert corporate waste into verified ESG outcomes, employee engagement, and measurable impact.",
    "initiatives", csr_body, ""),
"shop.html": ("Shop Upcycled Products — Support EmpowHer & Education",
    "Buy premium upcycled denim totes, backpacks, and corporate organizers handcrafted by EmpowHer artisans. Proceeds fund LEACT's education programs.",
    "shop", shop_body, ""),
"request-pickup.html": ("Request a Textile Pickup in Bengaluru | Reclaim Era",
    "Schedule a free pickup for clothes, household items, and stationery across Bengaluru. Contactless collection and donation receipts available.",
    "", pickup_body, ""),
"zero-waste-certification.html": ("Zero Waste Certification & AMC | SWM 2026 Compliance",
    "Turn your campus into a Zero Waste campus. End-to-end segregation, AMC, digital tracking and official Zero Waste Green Certificates for BWG compliance.",
    "zero", zero_body, ""),
"get-involved.html": ("Volunteer, Partner, Donate — Get Involved with Reclaim Era",
    "Join Reclaim Era: volunteer at Kogilu, sponsor EmpowHer training, donate equipment, or support education with tax-exempt donations.",
    "involved", involved_body, ""),
"resources.html": ("Resources & Reports — Blog, Case Studies, Downloads",
    "Practical guides, case studies, and impact reports on textile circularity, NEP 2020 education, and corporate waste programs.",
    "resources", resources_body, ""),
"contact.html": ("Contact Reclaim Era — Kogilu Hub & Corporate Partnerships",
    "Get in touch for pickups, CSR partnerships, school programs, or media inquiries. Direct CSR contact: reclaimera@gmail.com",
    "contact", contact_body, ""),
"campaign-application.html": ("Host a Donation Campaign | Reclaim Era",
    "Apply to host a Reclaim Era collection campaign at your apartment, school, college or business. \u20B9500 logistics fee, paid securely online.",
    "involved", campaign_body, ""),
"privacy-policy.html": ("Privacy Policy | Reclaim Era", "How Reclaim Era (LEACT) collects, uses and protects your information.", "", privacy_body, ""),
"terms.html": ("Terms & Conditions | Reclaim Era", "The terms that apply when you use the Reclaim Era website and services.", "", terms_body, ""),
"refund-policy.html": ("Refund & Cancellation Policy | Reclaim Era", "Refunds and cancellations for the Reclaim Era campaign logistics fee.", "", refund_body, ""),
"404.html": ("Page not found | Reclaim Era", "This page does not exist. Head back to the Reclaim Era home page.", "", notfound_body, ""),
}

for fname, (title, desc, active, body, extra) in PAGES.items():
    html = head(title, desc) + (extra or "") + header(active) + "\n<main>" + body + "</main>\n" + FOOTER
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname)

print("done:", len(PAGES), "pages")
