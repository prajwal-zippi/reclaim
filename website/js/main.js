/* Reclaim Era — interactions */
(function () {
  "use strict";

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Global landmarks and a discreet page-progress indicator. */
  const main = document.querySelector("main");
  if (main) {
    if (!main.id) main.id = "main-content";
    if (!document.querySelector(".skip-link")) {
      const skip = document.createElement("a");
      skip.className = "skip-link";
      skip.href = `#${main.id}`;
      skip.textContent = "Skip to main content";
      document.body.prepend(skip);
    }
  }
  const progress = document.createElement("div");
  progress.className = "page-progress";
  progress.setAttribute("aria-hidden", "true");
  document.body.prepend(progress);

  /* Decorative motion fields extend the circular Reclaim Era language across
     long pages without adding visual noise to every section. */
  document.querySelectorAll("main .section").forEach((section, index) => {
    if (index % 2 === 0 || section.classList.contains("impact-now")) return;
    section.classList.add("has-motion-field");
    const field = document.createElement("span");
    field.className = "motion-field";
    field.setAttribute("aria-hidden", "true");
    field.innerHTML = '<i class="motion-ring"></i><i class="motion-dot motion-dot-a"></i><i class="motion-dot motion-dot-b"></i>';
    section.prepend(field);
  });

  /* header shadow on scroll */
  const header = document.querySelector(".header");
  const onScroll = () => {
    if (header) header.classList.toggle("scrolled", window.scrollY > 8);
    const max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.transform = `scaleX(${max > 0 ? Math.min(window.scrollY / max, 1) : 0})`;
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* mobile nav toggle */
  const toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      document.body.classList.toggle("nav-open");
      const open = document.body.classList.contains("nav-open");
      toggle.setAttribute("aria-expanded", open);
      toggle.setAttribute("aria-label", open ? "Close menu" : "Menu");
    });
  }

  /* initiatives dropdown (click for touch / keyboard) */
  document.querySelectorAll(".nav .has-dropdown > .nav-link").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const li = btn.parentElement;
      const open = li.classList.toggle("open");
      btn.setAttribute("aria-expanded", open);
    });
  });
  document.addEventListener("click", (e) => {
    document.querySelectorAll(".nav li.open").forEach((li) => {
      if (!li.contains(e.target)) li.classList.remove("open");
    });
  });
  document.querySelectorAll(".nav a").forEach((link) => {
    link.addEventListener("click", () => {
      document.body.classList.remove("nav-open");
      if (toggle) {
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Menu");
      }
    });
  });
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    document.body.classList.remove("nav-open");
    document.querySelectorAll(".nav li.open").forEach((li) => {
      li.classList.remove("open");
      const trigger = li.querySelector(".nav-link");
      if (trigger) trigger.setAttribute("aria-expanded", "false");
    });
    if (toggle) {
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Menu");
    }
  });

  /* Do not expose dead social links until the client supplies real profiles. */
  document.querySelectorAll('.social-row a[href="#"]').forEach((link) => link.remove());

  /* reveal on scroll */
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            en.target.classList.add("in");
            io.unobserve(en.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("in"));
  }

  const sectionHeads = document.querySelectorAll(".section-head");
  if ("IntersectionObserver" in window && sectionHeads.length) {
    const headObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("motion-in");
        headObserver.unobserve(entry.target);
      });
    }, { threshold: 0.45 });
    sectionHeads.forEach((heading) => headObserver.observe(heading));
  } else {
    sectionHeads.forEach((heading) => heading.classList.add("motion-in"));
  }

  /* Pointer lighting and restrained depth, only on precise pointing devices. */
  if (!reducedMotion && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    document.addEventListener("pointermove", (event) => {
      document.documentElement.style.setProperty("--pointer-x", `${event.clientX}px`);
      document.documentElement.style.setProperty("--pointer-y", `${event.clientY}px`);
    }, { passive: true });

    const enhanceDepthCards = (root = document) => root.querySelectorAll(".step-card,.init-card,.feat-card,.prod-card,.impact-card,.gal-card,.partner-card").forEach((card) => {
      if (card.dataset.depthReady === "true") return;
      card.dataset.depthReady = "true";
      card.classList.add("depth-card");
      card.addEventListener("pointermove", (event) => {
        const box = card.getBoundingClientRect();
        const x = (event.clientX - box.left) / box.width;
        const y = (event.clientY - box.top) / box.height;
        card.style.setProperty("--card-x", `${x * 100}%`);
        card.style.setProperty("--card-y", `${y * 100}%`);
        card.style.setProperty("--tilt-x", `${(0.5 - y) * 3.5}deg`);
        card.style.setProperty("--tilt-y", `${(x - 0.5) * 3.5}deg`);
      });
      card.addEventListener("pointerleave", () => {
        card.style.removeProperty("--tilt-x");
        card.style.removeProperty("--tilt-y");
      });
    });
    enhanceDepthCards();
    document.querySelectorAll('[data-render]').forEach((region) => {
      new MutationObserver(() => enhanceDepthCards(region)).observe(region, { childList: true });
    });

    const heroVisual = document.querySelector(".hero-visual");
    if (heroVisual) {
      heroVisual.addEventListener("pointermove", (event) => {
        const box = heroVisual.getBoundingClientRect();
        heroVisual.style.setProperty("--hero-x", `${((event.clientX - box.left) / box.width - 0.5) * 14}px`);
        heroVisual.style.setProperty("--hero-y", `${((event.clientY - box.top) / box.height - 0.5) * 14}px`);
      });
      heroVisual.addEventListener("pointerleave", () => {
        heroVisual.style.setProperty("--hero-x", "0px");
        heroVisual.style.setProperty("--hero-y", "0px");
      });
    }

    /* A restrained magnetic response for primary actions. The movement is
       intentionally small so labels stay readable and buttons never feel
       detached from their layout position. */
    document.querySelectorAll(".header-cta .btn,.hero-ctas .btn").forEach((button) => {
      button.addEventListener("pointermove", (event) => {
        const box = button.getBoundingClientRect();
        const x = ((event.clientX - box.left) / box.width - 0.5) * 7;
        const y = ((event.clientY - box.top) / box.height - 0.5) * 7;
        button.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      });
      button.addEventListener("pointerleave", () => button.style.removeProperty("transform"));
    });
  }

  /* animated counters */
  const counters = document.querySelectorAll("[data-count]");
  const animate = (el) => {
    const target = parseFloat(el.dataset.count);
    const dur = 1800;
    const start = performance.now();
    const fmt = (n) =>
      el.dataset.format === "plain" ? Math.round(n) : Math.round(n).toLocaleString("en-IN");
    const tick = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(target * eased);
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ("IntersectionObserver" in window && counters.length) {
    const cio = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            animate(en.target);
            cio.unobserve(en.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((el) => cio.observe(el));
  } else {
    counters.forEach((el) => (el.textContent = (+el.dataset.count).toLocaleString("en-IN")));
  }

  /* accordions */
  document.querySelectorAll(".acc-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const item = btn.closest(".acc-item");
      const body = item.querySelector(".acc-body");
      const open = item.classList.toggle("open");
      btn.setAttribute("aria-expanded", open);
      body.style.maxHeight = open ? body.scrollHeight + "px" : "0";
    });
  });

  /* form submission via FormSubmit.co (AJAX; falls back to normal POST without JS) */
  document.querySelectorAll('form[action*="formsubmit.co"]').forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (form.classList.contains("newsletter")) {
        var subject = form.querySelector('input[name="_subject"]');
        if (subject) subject.value = "New subscriber — events, volunteering and impact reports";
        var interests = form.querySelector('input[name="interests"]');
        if (!interests) {
          interests = document.createElement("input");
          interests.type = "hidden";
          interests.name = "interests";
          form.appendChild(interests);
        }
        interests.value = "Future events; volunteering opportunities; news and impact reports";
      }
      const btn = form.querySelector('[type="submit"]');
      const ok = form.querySelector(".form-success");
      const err = form.querySelector(".form-error");
      if (ok) ok.classList.remove("show");
      if (err) err.classList.remove("show");
      const original = btn ? btn.innerHTML : "";
      form.setAttribute("aria-busy", "true");
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = "Sending…";
      }
      try {
        const res = await fetch(form.action.replace("formsubmit.co/", "formsubmit.co/ajax/"), {
          method: "POST",
          body: new FormData(form),
          headers: { Accept: "application/json" },
        });
        if (res.ok) {
          form.reset();
          if (ok) {
            ok.classList.add("show");
            ok.scrollIntoView({ behavior: "smooth", block: "nearest" });
          }
          if (form.classList.contains("newsletter")) {
            reToast("You’re subscribed for future events, volunteering opportunities and impact reports.");
          }
        } else {
          let msg = "";
          try {
            const data = await res.json();
            if (data && data.errors) msg = data.errors.map((x) => x.message).join(". ");
          } catch (_) {}
          if (err) {
            const slot = err.querySelector("[data-msg]");
            if (slot && msg) slot.textContent = msg;
            err.classList.add("show");
          }
          if (form.classList.contains("newsletter")) {
            reToast("We couldn’t subscribe you right now. Please try again.");
          }
        }
      } catch (_) {
        if (err) err.classList.add("show");
        if (form.classList.contains("newsletter")) {
          reToast("We couldn’t subscribe you right now. Please check your connection and retry.");
        }
      } finally {
        form.removeAttribute("aria-busy");
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = original;
        }
      }
    });
  });

  /* current year */
  document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

  /* Safety guard retained for any future external payment link placeholders.
     The campaign page's PayU button handles itself, so skip it here. */
  function reToast(msg) {
    var t = document.createElement("div");
    t.textContent = msg;
    t.style.cssText =
      "position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:300;" +
      "background:#17251E;color:#FAF6EE;padding:14px 20px;border-radius:12px;" +
      "box-shadow:0 14px 40px -12px rgba(0,0,0,.4);font:600 14px/1.4 Inter,sans-serif;" +
      "max-width:90%;text-align:center";
    document.body.appendChild(t);
    setTimeout(function () {
      t.style.transition = "opacity .4s";
      t.style.opacity = "0";
      setTimeout(function () { t.remove(); }, 400);
    }, 4200);
  }
  document.querySelectorAll("a[data-razorpay]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      if (a.id === "paySubmit") return;
      var href = a.getAttribute("href") || "";
      if (href.indexOf("REPLACE_WITH") > -1 || href === "#" || href === "") {
        e.preventDefault();
        reToast("Online payments open shortly. Please email reclaimera@gmail.com or call +91 81520 20145.");
      }
    });
  });
})();
