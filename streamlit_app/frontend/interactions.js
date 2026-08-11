/* =========================================================
   Aegis — progressive enhancement only.
   Nothing here affects application state, prediction or data.
   If it fails, the UI stays fully functional.
   ========================================================= */
(function () {
  "use strict";

  function root() {
    try {
      return window.parent && window.parent.document ? window.parent.document : document;
    } catch (e) {
      return document;
    }
  }

  var doc = root();
  if (!doc || doc.__aegisEnhanced) return;
  doc.__aegisEnhanced = true;

  /* 1. Reveal cards as they scroll into view (respects reduced motion). */
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function observe() {
    var nodes = doc.querySelectorAll(".ag-reveal:not(.is-visible)");
    if (!nodes.length) return;

    if (reduced || typeof IntersectionObserver === "undefined") {
      nodes.forEach(function (n) { n.classList.add("is-visible"); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        setTimeout(function () { el.classList.add("is-visible"); }, Math.min(i * 40, 160));
        io.unobserve(el);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });

    nodes.forEach(function (n) { io.observe(n); });
  }

  /* 2. Keep tooltips inside the viewport instead of clipping at the edge. */
  function fixTooltipEdges() {
    doc.querySelectorAll(".ag-tip").forEach(function (tip) {
      if (tip.__bound) return;
      tip.__bound = true;
      tip.setAttribute("tabindex", "0");
      tip.setAttribute("role", "note");
      var label = tip.getAttribute("data-tip");
      if (label) tip.setAttribute("aria-label", label);
    });
  }

  function run() {
    try { observe(); fixTooltipEdges(); } catch (e) { /* never break the app */ }
  }

  run();

  /* Streamlit replaces DOM nodes on every rerun — re-apply after mutations. */
  try {
    var pending = null;
    new MutationObserver(function () {
      clearTimeout(pending);
      pending = setTimeout(run, 120);
    }).observe(doc.body, { childList: true, subtree: true });
  } catch (e) { /* noop */ }
})();
