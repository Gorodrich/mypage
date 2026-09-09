# -*- coding: utf-8 -*-
"""
ファビコン・OGP 画像・Apple touch icon を生成する補助スクリプト。

    python tools/make_images.py

- assets/favicon.svg        … 元の名刺 SVG からロゴマークをそのまま切り出したベクタ
- assets/og.png             … OGP 用 1200x630(言語非依存の欧文のみ)
- assets/apple-touch-icon.png … 180x180

生成物はリポジトリにコミットされるので、通常のビルド(tools/build.py)では
実行不要です。ロゴやキャッチコピーを変えたときだけ再実行してください。
Pillow が必要です:  pip install pillow
"""
from __future__ import annotations

import io
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
SOURCE_SVG = os.path.join(ASSETS, "card-source.svg")

ACCENT = (9, 105, 218)
INK = (31, 35, 40)
MUTED = (89, 99, 110)
RULE = (209, 217, 224)
PAPER = (255, 255, 255)
INSET = (230, 232, 235)

MONO_OTF_URL = ("https://raw.githubusercontent.com/github/mona-sans/main/"
                "fonts/static/otf/MonaSansMono-%s.otf")


# ---------------------------------------------------------------------------
def make_favicon():
    """元 SVG のロゴマーク(gradient 込み)を、そのまま単体 SVG として書き出す。"""
    with open(SOURCE_SVG, encoding="utf-8") as fh:
        src = fh.read()
    body = src.split("</defs>", 1)[1]
    blocks = re.findall(r"<svg\b[^>]*>.*?</svg>", body, re.S)
    logo = blocks[-1]                                   # 最後の入れ子 svg = ロゴ
    inner = logo[len(re.match(r"<svg\b[^>]*>", logo).group(0)):-len("</svg>")]
    out = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'viewBox="0 0 400 400" width="400" height="400">'
        '<title>Gorodrich</title>'
        '<rect width="400" height="400" fill="#ffffff"/>'
        + inner.replace("<title>Gorodrich</title>", "") +
        "</svg>\n"
    )
    path = os.path.join(ASSETS, "favicon.svg")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    return path


# ---------------------------------------------------------------------------
def load_mono(weight, size):
    from PIL import ImageFont
    cache = os.path.join(HERE, "_fontcache")
    os.makedirs(cache, exist_ok=True)
    path = os.path.join(cache, "MonaSansMono-%s.otf" % weight)
    if not os.path.exists(path):
        with urllib.request.urlopen(MONO_OTF_URL % weight, timeout=60) as r:
            data = r.read()
        with open(path, "wb") as fh:
            fh.write(data)
    return ImageFont.truetype(path, size)


def draw_logo(draw, ox, oy, scale, color):
    """名刺のロゴマークを、400x400 の座標系からフラット 1 色で描き起こす。"""
    def s(v):
        return v * scale

    def rect(x0, y0, x1, y1):
        draw.rectangle([ox + s(x0), oy + s(y0), ox + s(x1), oy + s(y1)], fill=color)

    rect(0, 0, 80, 400)                       # 左の縦バー
    rect(0, 160, 280, 240)                    # 中央の横バー
    rect(160, 0, 240, 285)                    # 上から降りる縦バー
    draw.polygon([                            # 右上へ伸びる斜めの肩
        (ox + s(160), oy + s(0)), (ox + s(160), oy + s(5)),
        (ox + s(235), oy + s(80)), (ox + s(400), oy + s(80)),
        (ox + s(400), oy + s(0)),
    ], fill=color)
    # 右下のリング(外径 120 / 内径 40、中心 280,280)
    cx, cy = 280, 280
    draw.ellipse([ox + s(cx - 120), oy + s(cy - 120), ox + s(cx + 120), oy + s(cy + 120)],
                 fill=color)
    draw.ellipse([ox + s(cx - 40), oy + s(cy - 40), ox + s(cx + 40), oy + s(cy + 40)],
                 fill=(0, 0, 0, 0))


def make_og():
    from PIL import Image, ImageDraw
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), INSET)
    d = ImageDraw.Draw(img)

    # 名刺と同じ「白い紙 + ブルーバー」の構図
    pad = 56
    d.rectangle([pad, pad, W - pad, H - pad], fill=PAPER)
    d.rectangle([pad, pad, W - pad, pad + 26], fill=ACCENT)

    mark = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    draw_logo(ImageDraw.Draw(mark), 0, 0, 1.0, ACCENT + (255,))
    mark = mark.resize((150, 150), Image.LANCZOS)
    img.paste(mark, (112, 176), mark)

    x = 112
    d.text((x, 366), "GORODRICH", font=load_mono("SemiBold", 74), fill=INK)
    d.rectangle([x, 470, x + 460, 472], fill=RULE)
    d.text((x, 496), "Law by Day, Ops by Night", font=load_mono("Regular", 32), fill=MUTED)

    url = "56dri.ch"
    f = load_mono("Medium", 28)
    d.text((W - pad - 56 - d.textlength(url, font=f), 496), url, font=f, fill=ACCENT)

    path = os.path.join(ASSETS, "og.png")
    img.save(path, optimize=True)
    return path


def make_touch_icon():
    from PIL import Image, ImageDraw
    size = 180
    img = Image.new("RGB", (size, size), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, size, size], fill=ACCENT)

    mark = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    draw_logo(ImageDraw.Draw(mark), 0, 0, 1.0, (255, 255, 255, 255))
    mark = mark.resize((116, 116), Image.LANCZOS)
    img.paste(mark, ((size - 116) // 2, (size - 116) // 2), mark)

    path = os.path.join(ASSETS, "apple-touch-icon.png")
    img.save(path, optimize=True)
    return path


if __name__ == "__main__":
    print("  wrote", make_favicon())
    try:
        print("  wrote", make_og())
        print("  wrote", make_touch_icon())
    except ImportError:
        print("  skipped og.png / apple-touch-icon.png (Pillow が必要です)")
