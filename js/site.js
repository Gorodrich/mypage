/* 全ページ共通の小物。外部ライブラリなし。 */
(function () {
  "use strict";

  /* --- 言語ドロップダウン ------------------------------------------------
     マークアップは <details> なので JS が無くても開閉できる。
     ここでは「外側クリック」と Esc での閉じ動作だけを足す。 */
  var menus = Array.prototype.slice.call(document.querySelectorAll("[data-langmenu]"));

  function closeAll(except) {
    menus.forEach(function (m) {
      if (m !== except) m.open = false;
    });
  }

  menus.forEach(function (menu) {
    menu.addEventListener("toggle", function () {
      if (menu.open) closeAll(menu);
    });
  });

  if (menus.length) {
    document.addEventListener("click", function (event) {
      menus.forEach(function (menu) {
        if (menu.open && !menu.contains(event.target)) menu.open = false;
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key !== "Escape") return;
      menus.forEach(function (menu) {
        if (!menu.open) return;
        menu.open = false;
        var summary = menu.querySelector("summary");
        if (summary) summary.focus();
      });
    });
  }

  /* --- セクションナビの現在地表示 ---------------------------------------- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".sectionnav__link"));
  if (!navLinks.length || !("IntersectionObserver" in window)) return;

  var byId = {};
  var targets = [];
  navLinks.forEach(function (link) {
    var id = link.getAttribute("href").slice(1);
    var section = document.getElementById(id);
    if (!section) return;
    byId[id] = link;
    targets.push(section);
  });

  var visible = Object.create(null);

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      visible[entry.target.id] = entry.isIntersecting ? entry.intersectionRatio : 0;
    });
    var best = null;
    targets.forEach(function (section) {
      var ratio = visible[section.id] || 0;
      if (ratio > 0 && (!best || ratio > visible[best])) best = section.id;
    });
    navLinks.forEach(function (link) {
      link.classList.remove("is-active");
      link.removeAttribute("aria-current");
    });
    if (best && byId[best]) {
      byId[best].classList.add("is-active");
      byId[best].setAttribute("aria-current", "true");
    }
  }, { rootMargin: "-72px 0px -55% 0px", threshold: [0, 0.25, 0.5, 1] });

  targets.forEach(function (section) { observer.observe(section); });
})();
