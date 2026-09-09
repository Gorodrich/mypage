# 56dri.ch

紙の名刺の QR コードから辿り着く、デジタル名刺 + ポートフォリオサイトのソースコードです。
日本語・英語・中国語(簡体字)・韓国語の 4 言語対応。フレームワークなしの静的
HTML / CSS / JavaScript で、GitHub Pages から <https://56dri.ch> に公開しています。

> Source for a QR-linked digital business card and portfolio site, in Japanese,
> English, Simplified Chinese, and Korean. Static HTML/CSS/JS, no framework,
> served from GitHub Pages.

---

## 構成

```
/
├── index.html                名刺カード(日本語・既定)
├── en/ · zh/ · ko/           名刺カード(各言語)
├── portfolio/
│   ├── index.html            ポートフォリオ(日本語)
│   └── en/ · zh/ · ko/       ポートフォリオ(各言語)
│
├── css/
│   ├── tokens.css            デザイントークン + ベース + 共通コンポーネント
│   ├── card.css              名刺カードページ
│   └── portfolio.css         ポートフォリオページ
├── js/
│   ├── site.js               言語ドロップダウン、セクションナビの現在地表示
│   └── card.js               3D フリップ(タップ / 左右スワイプ / ←→ キー)
├── assets/
│   ├── card/                 言語別に生成した名刺面 SVG(front / back)
│   ├── card-source.svg       名刺の元デザイン(座標・配色の抽出元)
│   ├── fonts/                Mona Sans Mono VF + ライセンス
│   ├── goro_logo.svg
│   └── favicon.ico · og.png · apple-touch-icon.png
│
├── tools/                    ビルドスクリプトとコンテンツ定義(ページ生成元)
├── CNAME · robots.txt · sitemap.xml · .nojekyll
└── LICENSE · LICENSE-CONTENT · THIRD-PARTY-NOTICES.md
```

各ページの HTML と言語別の名刺 SVG は `tools/build.py` が生成します。
**`index.html` などを直接編集しても次回ビルドで上書きされます。**

---

## ローカルで見る

```bash
python -m http.server 8000
# → http://127.0.0.1:8000/
```

スタイルとスクリプトをルート絶対パス(`/css/...`)で参照しているため、
`file://` で直接開くと崩れます。必ずローカルサーバ経由で確認してください。

---

## ビルドと文言の編集

ページの文言は Python の標準ライブラリのみで組み立てています。外部パッケージは不要です。

| 変えたいもの | 編集するファイル |
|---|---|
| 名刺面の氏名・肩書き・所属・キャッチコピー | `tools/content.py` の `CARD` |
| メールアドレス・SNS・リンク先 | `tools/content.py` の `CONTACT` |
| ボタン・ヒント・meta 等の UI 文言 | `tools/content.py` の `UI` |
| ポートフォリオ本文 | `tools/content_pf/{ja,en,zh,ko}.py` |

```bash
python tools/build.py          # 全ページ + 名刺 SVG + sitemap.xml + CNAME を再生成
```

OGP 画像・favicon を作り直す場合のみ:

```bash
pip install pillow
python tools/make_images.py     # og.png · apple-touch-icon.png · favicon
```

---

## 実装メモ

**名刺カード**

- 初期表示はロゴ面。タップ / クリック、左右スワイプ(指に追従)、`←` `→` キー、
  ボタンでフリップし、往復できます。`transform: rotateY()` のみで、外部ライブラリなし。
- QR コードの位置には同じ言語の `/portfolio/` へのリンクを置いています。
- JavaScript を切った環境では、両面を上下に並べて表示します。

**名刺 SVG の多言語化**

- 座標・配色・罫線・アイコン・QR・ロゴは元デザインから抽出してそのまま引き継ぎ、
  テキストだけを言語別に組み直しています。元の字詰めは `letter-spacing`(em)で再現。
- 塗り足し込みの座標系のまま、`viewBox` で仕上がり寸法 55 × 91 mm を切り出しています。
- 氏名のローマ字表記・SNS・メール・QR は全言語共通です。

**共通**

- 言語ドロップダウンは `<details>` ベース。中身は実際の `<a href>` なので、
  JavaScript 無しでも切り替えられ、クローラからも辿れます。
- 各ページに `hreflang`(`x-default` は日本語)、`canonical`、OGP、`html lang` を設定。
- ブラウザ言語による自動リダイレクトはしていません。既定は常に日本語です。
- ライトモードのみ。`prefers-reduced-motion` を尊重します。

---

## フォント

| 用途 | フォント | 入手元 |
|---|---|---|
| 欧文(名刺・ラベル・コード) | Mona Sans Mono VF | [github/mona-sans](https://github.com/github/mona-sans) の公式 WOFF2 を同梱(SIL OFL 1.1) |
| 日本語 / 中国語(簡体字) / 韓国語 | Noto Sans JP / SC / KR | Google Fonts から実行時に読み込み |

---

## ライセンス

このリポジトリは **デュアルライセンス** です。

| 対象 | ライセンス | ファイル |
|---|---|---|
| ソースコード(HTML の構造、`css/`、`js/`、`tools/`) | MIT | [`LICENSE`](LICENSE) |
| サイトの文章・ロゴ・名刺デザイン・写真など制作物 | 著作権保持(All Rights Reserved) | [`LICENSE-CONTENT`](LICENSE-CONTENT) |
| 第三者由来(Primer Primitives、フォント) | 各ライセンスを継承 | [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md) |

コードを再利用する場合は、文章・`assets/goro_logo.svg`・名刺 SVG・個人情報を
すべて自分のものに差し替えてください。これらは MIT の対象外です。

`css/tokens.css` のトークン値は [primer/primitives](https://github.com/primer/primitives)
(MIT, © GitHub, Inc.)を抽出元にしています。詳細は
[`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md) を参照してください。
