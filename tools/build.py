# -*- coding: utf-8 -*-
"""
静的サイトジェネレータ(依存パッケージなし)。

    python tools/build.py

生成物:
    /index.html, /en/, /zh/, /ko/                     … 名刺カード(4 言語)
    /portfolio/, /portfolio/en/, /zh/, /ko/            … ポートフォリオ(4 言語)
    /assets/card/{lang}-{front,back}.svg               … 言語別の名刺面 SVG(単体でも表示可)
    /sitemap.xml

アイコン・ロゴ・QR コードのパスデータは、提供された元の名刺 SVG
(assets/名刺 ゴロードリヒ.svg)から実行時に抽出するので、
元デザインとの差異が生まれません。
"""
from __future__ import annotations

import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import content as C                      # noqa: E402
from content_pf import PORTFOLIO         # noqa: E402

SOURCE_SVG = os.path.join(ROOT, "assets", "card-source.svg")

E = lambda s: html.escape(str(s), quote=True)


# ---------------------------------------------------------------------------
# 元 SVG からの素材抽出
# ---------------------------------------------------------------------------
def extract_assets():
    """元の名刺 SVG から、入れ子の <svg> ブロック(アイコン群・QR・ロゴ)を順に取り出す。"""
    with open(SOURCE_SVG, encoding="utf-8") as fh:
        src = fh.read()
    body = src.split("</defs>", 1)[1]
    blocks = re.findall(r"<svg\b[^>]*>.*?</svg>", body, re.S)
    keys = ["mail", "github", "x", "note", "zenn", "qr", "logo"]
    if len(blocks) != len(keys):
        raise SystemExit(
            "元 SVG の構造が変わっています(入れ子 svg が %d 個、期待値 %d 個)"
            % (len(blocks), len(keys))
        )
    out = {}
    for key, block in zip(keys, blocks):
        open_tag = re.match(r"<svg\b[^>]*>", block).group(0)
        view_box = re.search(r'viewBox="([^"]+)"', open_tag).group(1)
        inner = block[len(open_tag): -len("</svg>")]
        inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S).strip()
        out[key] = {"viewBox": view_box, "inner": inner}
    return out


ART = extract_assets()


def sprite(key, x, y, size, fill=None, title=None, extra=""):
    a = ART[key]
    f = ' fill="%s"' % fill if fill else ""
    t = "<title>%s</title>" % E(title) if title else ""
    return (
        '<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="{vb}"{f} '
        'overflow="visible"{extra}>{t}{inner}</svg>'
    ).format(x=x, y=y, s=size, vb=a["viewBox"], f=f, t=t, inner=a["inner"], extra=extra)


# ---------------------------------------------------------------------------
# 名刺 SVG の組み立て
#   座標系は元データのカード座標(塗り足し込み 61.001 x 97.003mm)のまま。
#   viewBox で仕上がり寸法 55 x 91mm(= 3mm の塗り足しを落とした領域)を切り出す。
# ---------------------------------------------------------------------------
BLEED = 3.0
CARD_W, CARD_H = 61.001, 97.003
VIEWBOX = "%s %s %s %s" % (BLEED, BLEED, CARD_W - BLEED * 2, CARD_H - BLEED * 2)
CENTER = CARD_W / 2  # 30.5005

INK = "#1f2328"
MUTED = "#59636e"
ACCENT = "#0969da"
RULE = "#d1d9e0"

SVG_STYLE = """.bc-mono{{font-family:"Mona Sans Mono VF",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
.bc-cjk{{font-family:{cjk}}}
.bc-text{{white-space:pre}}"""


def text(s, x, y, *, font="mono", size=2.3, weight=400, fill=INK,
         anchor="start", ls=0.0, cls=""):
    """1 本のテキスト行。元データの字詰めは letter-spacing(em)で再現する。"""
    if not s:
        return ""
    attrs = [
        'class="bc-text bc-%s%s"' % (font, (" " + cls) if cls else ""),
        'x="%s"' % round(x + (ls * size / 2 if anchor == "middle" else 0), 4),
        'y="%s"' % y,
        'font-size="%s"' % size,
        'font-weight="%s"' % weight,
        'fill="%s"' % fill,
    ]
    if anchor != "start":
        attrs.append('text-anchor="%s"' % anchor)
    if ls:
        attrs.append('letter-spacing="%sem"' % ls)
    return "<text %s>%s</text>" % (" ".join(attrs), E(s))


# 情報面の連絡先行: (キー, アイコン x, アイコン y, アイコン寸法, テキスト x, テキスト y,
#                    文字サイズ, 当たり判定 x, 当たり判定 y, 当たり判定 w, 当たり判定 h)
CONTACT_ROWS = [
    ("email",  9.0,    48.880, 3.398, 14.396, 51.505, 2.5,  8.0, 47.60, 44.0, 5.2),
    ("github", 9.0,    55.697, 3.398, 14.197, 58.190, 2.3,  8.0, 54.60, 21.9, 5.1),
    ("x",      31.499, 55.796, 3.200, 36.497, 58.190, 2.3, 30.6, 54.60, 21.4, 5.1),
    ("note",   9.0,    61.692, 3.398, 14.197, 64.185, 2.3,  8.0, 60.60, 21.9, 5.1),
    ("zenn",   31.499, 61.692, 3.398, 36.696, 64.185, 2.3, 30.6, 60.60, 21.4, 5.1),
]
ICON_KEY = {"email": "mail", "github": "github", "x": "x", "note": "note", "zenn": "zenn"}



def build_front(lang, *, interactive, portfolio_href="/portfolio/"):
    card = C.CARD[lang]
    ui = C.UI[lang]
    p = []

    # 上部のブルーバー(塗り足しまで伸ばす)
    p.append('<rect x="0" y="0" width="%s" height="5.999" fill="%s"/>' % (CARD_W, ACCENT))

    nm, ns = card["name_main"], card["name_sub"]
    p.append(text(nm["text"], 9, 16.818, font=nm["font"], size=nm["size"],
                  weight=nm["weight"], fill=INK, ls=nm.get("ls", 0)))
    p.append(text(ns["text"], 9, 22.375, font=ns["font"], size=ns["size"],
                  weight=ns["weight"], fill=MUTED, ls=ns.get("ls", 0)))

    for line, y in zip(card["title"], (29.783, 32.884)):
        p.append(text(line["text"], 9, y, font=line["font"], size=line["size"],
                      weight=line["weight"], fill=ACCENT))

    af = card["affiliation"]
    p.append(text(af["text"], 9, 38.978, font=af["font"], size=af["size"],
                  weight=af["weight"], fill=INK))

    p.append('<rect x="9" y="44.613" width="43.001" height="0.248" fill="%s"/>' % RULE)

    # --- 連絡先 -------------------------------------------------------------
    for key, ix, iy, isz, tx, ty, ts, hx, hy, hw, hh in CONTACT_ROWS:
        info = C.CONTACT[key]
        row = sprite(ICON_KEY[key], ix, iy, isz, fill=INK, extra=' class="bc-icon"')
        row += text(info["id"], tx, ty, font="mono", size=ts, fill=INK)
        if interactive:
            label = ui["email_label"] if key == "email" else info["href"]
            hit = (
                '<rect class="bc-hit" x="%s" y="%s" width="%s" height="%s" rx="1.2"/>'
                % (hx, hy, hw, hh)
            )
            rel = "" if key == "email" else ' target="_blank" rel="me noopener"'
            row = (
                '<a class="bc-link" href="%s"%s aria-label="%s">%s%s</a>'
                % (E(info["href"]), rel, E("%s: %s" % (label, info["id"])), hit, row)
            )
        p.append(row)

    # --- ポートフォリオへの CTA ボタン -----------------------------------
    cta = '<rect class="bc-cta-bg" x="9" y="76" width="43.001" height="7.4" rx="1.6"/>'
    cta += ('<text class="bc-text bc-%s bc-cta-label" x="%s" y="80.7"'
            ' font-size="2.7" font-weight="600" fill="#ffffff" text-anchor="middle"'
            ' letter-spacing="0.03em">%s<tspan aria-hidden="true"> →</tspan></text>'
            % (card["tagline"]["font"], CENTER, E(ui["portfolio_cta"])))
    if interactive:
        cta = ('<a class="bc-link bc-link--cta" href="%s" aria-label="%s">%s</a>'
               % (E(portfolio_href), E(ui["qr_label"]), cta))
    p.append(cta)

    return "".join(p)


def build_back(lang, *, interactive=False):
    card = C.CARD[lang]
    p = []
    p.append(sprite("logo", 18.501, 29.775, 24, title="Gorodrich"))
    p.append(text(C.WORDMARK, CENTER, 62.949, font="mono", size=3.0, weight=500,
                  fill=INK, anchor="middle", ls=0.3))
    p.append('<rect x="22.499" y="66.405" width="16" height="0.248" fill="%s"/>' % RULE)
    tl = card["tagline"]
    p.append(text(tl["text"], CENTER, 71.432, font=tl["font"], size=tl["size"],
                  weight=tl["weight"], fill=MUTED, anchor="middle", ls=tl.get("ls", 0)))
    # 下部のブルーバー
    p.append('<rect x="0" y="91.004" width="%s" height="5.999" fill="%s"/>' % (CARD_W, ACCENT))
    return "".join(p)


def card_svg(lang, face, *, standalone, portfolio_href="/portfolio/", role_label=""):
    body = (build_front(lang, interactive=not standalone, portfolio_href=portfolio_href)
            if face == "front" else build_back(lang))
    head = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s"' % VIEWBOX,
        ' class="bc bc--%s"' % face,
    ]
    if standalone:
        head.append(' xmlns:xlink="http://www.w3.org/1999/xlink" width="55mm" height="91mm"')
    if role_label:
        head.append(' role="img" aria-label="%s"' % E(role_label))
    head.append(">")
    style = ""
    if standalone:
        # 単体表示用。Web ページ内に埋め込むときは css/card.css 側で指定する。
        style = "<style>%s</style>" % SVG_STYLE.format(cjk=C.CJK_STACK[lang])
    return "".join(head) + style + body + "</svg>"


# ---------------------------------------------------------------------------
# URL ヘルパ
# ---------------------------------------------------------------------------
def card_url(lang):
    return "/" + C.LANG_META[lang]["card_prefix"]


def pf_url(lang):
    return "/portfolio/" + C.LANG_META[lang]["pf_prefix"]


def page_url(kind, lang):
    return card_url(lang) if kind == "card" else pf_url(lang)


# ---------------------------------------------------------------------------
# 共通の HTML パーツ
# ---------------------------------------------------------------------------
GOOGLE_FONTS = {
    "ja": "family=Noto+Sans+JP:wght@400;500;600;700",
    "en": "family=Noto+Sans+JP:wght@400;500;600;700",
    "zh": "family=Noto+Sans+SC:wght@400;500;600;700",
    "ko": "family=Noto+Sans+KR:wght@400;500;600;700",
}


def head(kind, lang, *, title, desc, stylesheet):
    m = C.LANG_META[lang]
    url = C.SITE["origin"] + page_url(kind, lang)
    alts = "".join(
        '\n  <link rel="alternate" hreflang="%s" href="%s%s">'
        % (C.LANG_META[l]["hreflang"], C.SITE["origin"], page_url(kind, l))
        for l in C.LANGS
    )
    alts += ('\n  <link rel="alternate" hreflang="x-default" href="%s%s">'
             % (C.SITE["origin"], page_url(kind, "ja")))
    return """<!doctype html>
<html lang="{htmllang}" class="no-js">
<head>
  <meta charset="utf-8">
  <script>document.documentElement.classList.remove('no-js');</script>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">{alts}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="GORODRICH">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="{oglocale}">
  <meta property="og:image" content="{origin}/assets/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0969da">
  <link rel="icon" href="/assets/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/MonaSansMonoVF.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?{gfonts}&display=swap">
  <link rel="stylesheet" href="/css/tokens.css">
  <link rel="stylesheet" href="/css/{stylesheet}">
</head>
""".format(
        htmllang=m["html"], title=E(title), desc=E(desc), url=url, alts=alts,
        oglocale={"ja": "ja_JP", "en": "en_US", "zh": "zh_CN", "ko": "ko_KR"}[lang],
        origin=C.SITE["origin"], gfonts=GOOGLE_FONTS[lang], stylesheet=stylesheet,
    )


def lang_menu(kind, lang):
    ui = C.UI[lang]
    items = []
    for l in C.LANGS:
        cur = l == lang
        items.append(
            '<li><a class="langmenu__item{c}" href="{href}" hreflang="{hl}" lang="{hl}"{aria}>'
            '<span class="langmenu__check" aria-hidden="true">{mark}</span>{label}</a></li>'.format(
                c=" is-current" if cur else "",
                href=page_url(kind, l),
                hl=C.LANG_META[l]["hreflang"],
                aria=' aria-current="true"' if cur else "",
                mark="&#10003;" if cur else "",
                label=E(C.LANG_META[l]["label"]),
            )
        )
    return """<details class="langmenu" data-langmenu>
        <summary class="langmenu__button" aria-label="{menu}: {current}">
          <svg class="langmenu__globe" viewBox="0 0 16 16" width="15" height="15" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.25"><circle cx="8" cy="8" r="6.3"/><ellipse cx="8" cy="8" rx="2.7" ry="6.3"/><path d="M2 5.8h12M2 10.2h12"/></svg>
          <span class="langmenu__label">{label}</span>
          <svg class="langmenu__caret" viewBox="0 0 16 16" width="12" height="12" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6.5 8 10.5l4-4"/></svg>
        </summary>
        <div class="langmenu__panel">
          <p class="langmenu__title">{menu}</p>
          <ul class="langmenu__list">{items}</ul>
        </div>
      </details>""".format(
        menu=E(ui["lang_menu"]), current=E(C.LANG_META[lang]["label"]),
        label=E(C.LANG_META[lang]["label"]), items="".join(items),
    )


# ---------------------------------------------------------------------------
# 名刺カードページ
# ---------------------------------------------------------------------------
def build_card_page(lang):
    ui = C.UI[lang]
    front = card_svg(lang, "front", standalone=False, portfolio_href=pf_url(lang))
    back = card_svg(lang, "back", standalone=False)
    return head("card", lang, title=ui["card_title"], desc=ui["card_desc"],
                stylesheet="card.css") + """<body class="page page--card" data-lang="{lang}">
  <a class="skip-link" href="#card">{flip}</a>
  <header class="topbar">
    <a class="topbar__brand" href="{cardurl}">GORODRICH</a>
    {menu}
  </header>

  <main class="stage">
    <div class="scene">
      <div class="card" id="card" data-face="logo">
        <div class="card__face card__face--logo" role="group" aria-label="{facelogo}">{back}</div>
        <div class="card__face card__face--info" role="group" aria-label="{faceinfo}">{front}</div>
      </div>
    </div>

    <div class="stage__controls">
      <button type="button" class="btn btn--primary" id="flip-button"
              data-label-info="{toinfo}" data-label-logo="{tologo}"
              aria-controls="card" aria-pressed="false">{toinfo}</button>
      <p class="hint" id="flip-hint">{hint}</p>
    </div>
  </main>

  <p class="sr-only" role="status" aria-live="polite" id="face-status">{facelogo}</p>
  <script src="/js/site.js" defer></script>
  <script src="/js/card.js" defer></script>
</body>
</html>
""".format(
        lang=lang, cardurl=card_url(lang), pfurl=pf_url(lang), menu=lang_menu("card", lang),
        back=back, front=front, facelogo=E(ui["face_logo"]), faceinfo=E(ui["face_info"]),
        toinfo=E(ui["flip_to_info"]), tologo=E(ui["flip_to_logo"]),
        hint=E(ui["hint"]), flip=E(ui["flip_to_info"]),
    )


# ---------------------------------------------------------------------------
# ポートフォリオページ
# ---------------------------------------------------------------------------
def level_meter(level, label):
    dots = "".join(
        '<span class="meter__dot%s"></span>' % (" is-on" if i < level else "")
        for i in range(5)
    )
    return ('<span class="meter" role="img" aria-label="%s: %d / 5">%s</span>'
            % (E(label), level, dots))


def section_about(data, ui):
    d = data["about"]
    facts = "".join(
        '<div class="fact"><dt class="fact__label">%s</dt><dd class="fact__value">%s</dd></div>'
        % (E(f["label"]), E(f["value"])) for f in d["facts"]
    )
    paras = "".join("<p>%s</p>" % E(p) for p in d["paragraphs"])
    values = "".join(
        '<li class="value"><h3 class="value__title">%s</h3><p class="value__body">%s</p></li>'
        % (E(v["title"]), E(v["body"])) for v in d["values"]
    )
    return """
      <p class="lead">{lead}</p>
      <div class="about">
        <div class="about__prose prose">{paras}</div>
        <dl class="facts">{facts}</dl>
      </div>
      <h3 class="subheading">{vh}</h3>
      <ul class="values">{values}</ul>""".format(
        lead=E(d["lead"]), paras=paras, facts=facts,
        vh=E(d["values_heading"]), values=values)


def section_career(data, ui):
    d = data["career"]
    items = []
    for it in d["items"]:
        points = "".join("<li>%s</li>" % E(p) for p in it["points"])
        tags = "".join('<li class="tag">%s</li>' % E(t) for t in it["tags"])
        items.append("""
        <li class="entry">
          <p class="entry__period">{period}</p>
          <div class="entry__body">
            <h3 class="entry__org">{org}</h3>
            <p class="entry__role">{role}</p>
            <p class="entry__summary">{summary}</p>
            <ul class="entry__points">{points}</ul>
            <ul class="tags">{tags}</ul>
          </div>
        </li>""".format(period=E(it["period"]), org=E(it["org"]), role=E(it["role"]),
                        summary=E(it["summary"]), points=points, tags=tags))
    return ('<p class="section__intro">%s</p><ol class="timeline">%s</ol>'
            % (E(d["intro"]), "".join(items)))


def section_skills(data, ui):
    d = data["skills"]
    groups = []
    for g in d["groups"]:
        rows = "".join("""
            <li class="skill">
              <div class="skill__head"><span class="skill__name">{name}</span>{meter}</div>
              <p class="skill__note">{note}</p>
            </li>""".format(name=E(i["name"]), note=E(i["note"]),
                            meter=level_meter(i["level"], ui["skill_level"]))
            for i in g["items"])
        groups.append('<section class="skillgroup"><h3 class="skillgroup__name">%s</h3>'
                      '<ul class="skills">%s</ul></section>' % (E(g["name"]), rows))
    return ('<p class="section__intro">%s</p><div class="skillgrid">%s</div>'
            % (E(d["intro"]), "".join(groups)))


def section_works(data, ui, lang):
    d = data["works"]
    cards = []
    for w in d["items"]:
        stack = "".join('<li class="tag tag--stack">%s</li>' % E(s) for s in w.get("stack", []))
        hi = "".join("<li>%s</li>" % E(h) for h in w["highlights"])
        link_items = w.get("links") or ([w["link"]] if w.get("link") else [])
        link = ""
        for li in link_items:
            href = li["href"]
            if href == "CARD_URL":
                href = card_url(lang)
            ext = href.startswith("http")
            link += ('<p class="work__link"><a class="textlink" href="%s"%s>%s'
                     '<span aria-hidden="true"> &rarr;</span></a></p>'
                     % (E(href), ' target="_blank" rel="noopener"' if ext else "",
                        E(li["label"])))
        cards.append("""
        <article class="work">
          <header class="work__head">
            <h3 class="work__title">{title}</h3>
            <p class="work__tagline">{tagline}</p>
          </header>
          <dl class="work__meta">
            <div><dt>{lrole}</dt><dd>{role}</dd></div>
            <div><dt>{lperiod}</dt><dd>{period}</dd></div>
          </dl>
          <p class="work__body">{body}</p>
          <ul class="work__highlights">{hi}</ul>
          {stackblock}
          {link}
        </article>""".format(
            title=E(w["title"]), tagline=E(w["tagline"]), role=E(w["role"]),
            period=E(w["period"]), body=E(w["body"]), hi=hi, link=link,
            stackblock=('<p class="work__stacklabel">%s</p><ul class="tags">%s</ul>'
                        % (E(ui["stack"]), stack)) if stack else "",
            lrole=E(ui["role"]), lperiod=E(ui["period"]), lstack=E(ui["stack"])))
    return ('<p class="section__intro">%s</p><div class="works">%s</div>'
            % (E(d["intro"]), "".join(cards)))


def build_portfolio_page(lang):
    ui = C.UI[lang]
    data = PORTFOLIO[lang]
    renderers = {
        "about": lambda: section_about(data, ui),
        "career": lambda: section_career(data, ui),
        "skills": lambda: section_skills(data, ui),
        "works": lambda: section_works(data, ui, lang),
    }
    nav = "".join(
        '<li><a class="sectionnav__link" href="#%s">%s</a></li>' % (s["id"], E(s["nav"]))
        for s in data["sections"]
    )
    sections = "".join("""
    <section class="section" id="{sid}" aria-labelledby="{sid}-h">
      <div class="wrap">
        <header class="section__head">
          <p class="section__index">{idx}</p>
          <h2 class="section__title" id="{sid}-h">{heading}</h2>
        </header>
        {inner}
      </div>
    </section>""".format(sid=s["id"], idx="%02d" % (n + 1), heading=E(s["heading"]),
                         inner=renderers[s["id"]]())
        for n, s in enumerate(data["sections"]))

    return head("portfolio", lang, title=ui["pf_title"], desc=ui["pf_desc"],
                stylesheet="portfolio.css") + """<body class="page page--portfolio" data-lang="{lang}">
  <a class="skip-link" href="#about">{toc}</a>
  <header class="topbar topbar--sticky">
    <a class="topbar__brand" href="{cardurl}">GORODRICH</a>
    <div class="topbar__end">
      <a class="topbar__back textlink" href="{cardurl}">
        <span aria-hidden="true">&larr; </span>{back}</a>
      {menu}
    </div>
  </header>

  <main id="main">
    <div class="hero">
      <div class="wrap">
        <p class="hero__kicker">{kicker}</p>
        <h1 class="hero__title">{name}</h1>
        <p class="hero__lead">{lead}</p>
        <nav class="sectionnav" aria-label="{toc}">
          <ul class="sectionnav__list">{nav}</ul>
        </nav>
      </div>
    </div>
{sections}
  </main>

  <footer class="footer">
    <div class="wrap footer__inner">
      <p class="footer__links">
        <a class="textlink" href="{cardurl}">{back}</a>
        <a class="textlink" href="#main">{top}</a>
      </p>
      <p class="footer__copy">&copy; GORODRICH</p>
      <p class="footer__note">{note}</p>
      <p class="footer__license">
        <a class="textlink" href="{blob}/LICENSE" target="_blank" rel="noopener">{lic_code}</a>
        <a class="textlink" href="{blob}/LICENSE-CONTENT" target="_blank" rel="noopener">{lic_content}</a>
        <a class="textlink" href="{blob}/THIRD-PARTY-NOTICES.md" target="_blank" rel="noopener">{lic_third}</a>
      </p>
    </div>
  </footer>
  <script src="/js/site.js" defer></script>
</body>
</html>
""".format(
        lang=lang, cardurl=card_url(lang), menu=lang_menu("portfolio", lang),
        back=E(ui["back_to_card"]), kicker=E(ui["pf_kicker"]),
        name=E(C.CARD[lang]["name_main"]["text"] if C.CARD[lang]["name_main"]["font"] == "cjk"
              else C.WORDMARK),
        lead=E(ui["pf_lead"]), nav=nav, toc=E(ui["toc"]), sections=sections,
        note=E(ui["footer_note"]), top=E(ui["top"]),
        lic_code=E(ui["lic_code"]), lic_content=E(ui["lic_content"]),
        lic_third=E(ui["lic_third"]), blob=E(C.SITE["repo_blob"]),
    )


# ---------------------------------------------------------------------------
def write(relpath, body):
    path = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    return relpath


def build_sitemap():
    urls = []
    for kind in ("card", "portfolio"):
        for lang in C.LANGS:
            loc = C.SITE["origin"] + page_url(kind, lang)
            alts = "".join(
                '\n    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>'
                % (C.LANG_META[l]["hreflang"], C.SITE["origin"], page_url(kind, l))
                for l in C.LANGS
            )
            urls.append("  <url>\n    <loc>%s</loc>%s\n    <priority>%s</priority>\n  </url>"
                        % (loc, alts, "1.0" if kind == "card" else "0.8"))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def main():
    written = []
    for lang in C.LANGS:
        for face in ("front", "back"):
            written.append(write(
                "assets/card/%s-%s.svg" % (lang, face),
                card_svg(lang, face, standalone=True, portfolio_href=pf_url(lang),
                         role_label=C.UI[lang]["face_info" if face == "front" else "face_logo"]),
            ))
        written.append(write(C.LANG_META[lang]["card_prefix"] + "index.html",
                             build_card_page(lang)))
        written.append(write("portfolio/" + C.LANG_META[lang]["pf_prefix"] + "index.html",
                             build_portfolio_page(lang)))
    written.append(write("sitemap.xml", build_sitemap()))
    written.append(write("robots.txt",
                         "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n"
                         % C.SITE["origin"]))
    written.append(write("CNAME", C.SITE["domain"] + "\n"))
    for f in written:
        print("  wrote", f)
    print("%d files." % len(written))


if __name__ == "__main__":
    main()
