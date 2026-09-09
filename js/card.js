/* 名刺カードの 3D フリップ。CSS transform だけで動かす(外部ライブラリなし)。 */
(function () {
  "use strict";

  var card = document.getElementById("card");
  var button = document.getElementById("flip-button");
  var status = document.getElementById("face-status");
  if (!card) return;

  var faces = {
    logo: card.querySelector(".card__face--logo"),
    info: card.querySelector(".card__face--info")
  };
  var LABELS = {
    info: button ? button.getAttribute("data-label-logo") : "",   // 情報面 → 戻る
    logo: button ? button.getAttribute("data-label-info") : ""    // ロゴ面 → 見る
  };
  var SWIPE_THRESHOLD = 45;   // px。これ以上の横移動でフリップ確定
  var TAP_SLOP = 8;           // px。これ未満ならタップ扱い
  var MAX_DRAG_DEG = 220;     // deg。ドラッグ追従の上限(行き過ぎ防止)

  /* カードの現在角度(連続値)。表示は常にこの値から組み立てる。 */
  var rotation = card.dataset.face === "info" ? 180 : 0;

  function setTransform(deg) {
    card.style.transform = "rotateY(" + deg + "deg)";
  }

  /* 角度から見えている面を求める(180 の倍数ごとに反転) */
  function faceForRotation(deg) {
    return Math.abs(Math.round(deg / 180) % 2) === 1 ? "info" : "logo";
  }

  /* --- 面の切り替え(a11y 状態のみ。見た目は setTransform が担当) --------- */
  function apply(face) {
    card.dataset.face = face;

    // 裏返っている面のリンクはフォーカスを受けないようにする
    Object.keys(faces).forEach(function (key) {
      var el = faces[key];
      if (!el) return;
      var hidden = key !== face;
      el.setAttribute("aria-hidden", hidden ? "true" : "false");
      if ("inert" in HTMLElement.prototype) {
        el.inert = hidden;
      } else {
        el.querySelectorAll("a").forEach(function (a) {
          if (hidden) { a.setAttribute("tabindex", "-1"); }
          else { a.removeAttribute("tabindex"); }
        });
      }
    });

    if (button) {
      button.textContent = LABELS[face];
      button.setAttribute("aria-pressed", face === "info" ? "true" : "false");
    }
    if (status) {
      var el = faces[face];
      status.textContent = el ? el.getAttribute("aria-label") || "" : "";
    }
  }

  /* dir > 0 で正方向、dir < 0 で逆方向に半回転 */
  function flip(dir) {
    rotation += (dir < 0 ? -180 : 180);
    apply(faceForRotation(rotation));
    setTransform(rotation);
  }

  /* トランジションを一旦戻してから角度を当てる(確実にアニメーションさせる) */
  function animateTo(deg) {
    card.classList.remove("is-dragging");
    void card.offsetWidth;   // reflow
    setTransform(deg);
  }

  apply(faceForRotation(rotation));
  setTransform(rotation);
  card.setAttribute("aria-live", "off");

  if (button) {
    button.addEventListener("click", function () { flip(1); });
  }

  /* --- ポインタ操作: タップ / クリック / 左右スワイプ ---------------------- */
  var drag = null;

  function isInteractive(target) {
    return !!(target.closest && target.closest("a, button"));
  }

  card.addEventListener("pointerdown", function (event) {
    if (event.button !== 0 && event.pointerType === "mouse") return;
    drag = {
      id: event.pointerId,
      x: event.clientX,
      y: event.clientY,
      dx: 0,
      dy: 0,
      onLink: isInteractive(event.target),
      moved: false,
      start: rotation,
      // 幅は transform の影響を受けない offsetWidth で一度だけ取る
      span: card.offsetWidth || card.getBoundingClientRect().width || 1
    };
  });

  card.addEventListener("pointermove", function (event) {
    if (!drag || event.pointerId !== drag.id) return;
    drag.dx = event.clientX - drag.x;
    drag.dy = event.clientY - drag.y;

    if (!drag.moved && Math.abs(drag.dx) > TAP_SLOP && Math.abs(drag.dx) > Math.abs(drag.dy)) {
      drag.moved = true;
      card.classList.add("is-dragging");
      card.setPointerCapture(drag.id);
    }
    if (!drag.moved) return;

    // 指(カーソル)の動きにそのまま追従させる。
    var delta = (drag.dx / drag.span) * 180;
    if (delta > MAX_DRAG_DEG) delta = MAX_DRAG_DEG;
    else if (delta < -MAX_DRAG_DEG) delta = -MAX_DRAG_DEG;
    setTransform(drag.start + delta);
  });

  function endDrag(event) {
    if (!drag || event.pointerId !== drag.id) return;
    var moved = drag.moved;
    var dx = drag.dx;
    var start = drag.start;
    var onLink = drag.onLink;
    drag = null;

    if (moved) {
      if (Math.abs(dx) >= SWIPE_THRESHOLD) {
        // 動かした向きへそのまま半回転を完了させる
        rotation = start + (dx > 0 ? 180 : -180);
        apply(faceForRotation(rotation));
        animateTo(rotation);
      } else {
        // 戻す
        rotation = start;
        animateTo(rotation);
      }
      return;
    }

    card.classList.remove("is-dragging");
    // 動いていない = タップ。リンク上のタップはリンクに任せる。
    if (!onLink) flip(1);
  }

  card.addEventListener("pointerup", endDrag);
  card.addEventListener("pointercancel", function (event) {
    if (!drag || event.pointerId !== drag.id) return;
    var start = drag.start;
    drag = null;
    rotation = start;
    animateTo(rotation);
  });

  /* --- キーボード ---------------------------------------------------------- */
  document.addEventListener("keydown", function (event) {
    if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
    var tag = document.activeElement && document.activeElement.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
    if (document.activeElement && document.activeElement.closest("[data-langmenu][open]")) return;
    event.preventDefault();
    flip(event.key === "ArrowLeft" ? -1 : 1);
  });
})();
