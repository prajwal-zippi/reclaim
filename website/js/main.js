/* Reclaim Era — interactions */
(function () {
  "use strict";

  /* header shadow on scroll */
  const header = document.querySelector(".header");
  const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 8);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* mobile nav toggle */
  const toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", document.body.classList.contains("nav-open"));
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
      const btn = form.querySelector('[type="submit"]');
      const ok = form.querySelector(".form-success");
      const err = form.querySelector(".form-error");
      if (ok) ok.classList.remove("show");
      if (err) err.classList.remove("show");
      const original = btn ? btn.innerHTML : "";
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
        }
      } catch (_) {
        if (err) err.classList.add("show");
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = original;
        }
      }
    });
  });

  /* current year */
  document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

  /* Razorpay payment links: friendly guard until the real links are pasted in.
     The campaign page's pay button (#paySubmit) handles itself, so skip it here. */
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
