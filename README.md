# 56dri.ch

紙の名刺に印字された QR コードからアクセスする、デジタル名刺兼ポートフォリオサイトのソースコードです。
日本語・英語・簡体字中国語・韓国語の 4 言語に対応しています。フレームワークを使用しない純粋な HTML / CSS / JavaScript で構築され、GitHub Pages 経由で <https://56dri.ch> に公開されています。

> Source for a QR-linked digital business card and portfolio site, in Japanese, English, Simplified Chinese, and Korean. Static HTML/CSS/JS, no framework, served from GitHub Pages.

- **公開 URL**：<https://56dri.ch>
- **対象環境**：Python 3.13（ビルド時） / モダンブラウザ
- **対応言語**：日本語（`ja`）、英語（`en`）、簡体字中国語（`zh`）、韓国語（`ko`）
- **主な特徴**：フレームワーク不使用（Vanilla HTML/CSS/JS）、名刺3Dフリップ、標準ライブラリ中心の静的サイト生成

## 目次

- [概要](#概要)
- [主な機能](#主な機能)
- [設計と実装仕様](#設計と実装仕様)
  - [名刺カード](#名刺カード)
  - [名刺 SVG の多言語化](#名刺-svg-の多言語化)
  - [フォント](#フォント)
  - [共通仕様](#共通仕様)
- [ディレクトリ構成](#ディレクトリ構成)
- [開発](#開発)
  - [前提環境](#前提環境)
  - [ローカル実行](#ローカル実行)
  - [コンテンツの編集箇所](#コンテンツの編集箇所)
  - [ビルドコマンド](#ビルドコマンド)
  - [画像の再生成](#画像の再生成)
- [ドキュメント](#ドキュメント)
- [ライセンス](#ライセンス)

## 概要

本プロジェクトは、オフラインで手渡す紙の名刺とオンライン上の制作物・活動実績をシームレスにつなぐ、個人のデジタルプレゼンスの拠点です。

外部フレームワーク（React や Vue 等）や重厚なビルドツールに依存せず、ブラウザ標準の Web 標準技術（Vanilla HTML/CSS/JS）と Python 標準ライブラリによる最小限の静的サイトジェネレーターで構築されています。高信頼性・高速読み込み・長期的な保守性を重視した設計です。

## 主な機能

| 機能 | 概要 |
|---|---|
| 名刺3Dフリップ | タップ・クリック、左右スワイプ（指に追従）、`←` `→` キー操作で滑らかに反転する名刺カード |
| 4言語対応 | 日本語・英語・簡体字中国語・韓国語の完全ローカライズ（HTML および名刺面 SVG） |
| ポートフォリオ | プロジェクト実績、スキル、経歴を整理した詳細紹介ページ |
| 標準ライブラリSSG | Python 標準機能のみで HTML 生成・名刺 SVG 組版・サイトマップ生成を実行（外部パッケージ不要） |
| アクセシビリティ・SEO | 各言語の `hreflang` / `canonical` / OGP 最適化、NoScript 環境でのフォールバック表示 |

## 設計と実装仕様

### 名刺カード

- 初期表示はロゴ面。タップ / クリック、左右スワイプ（指に追従）、`←` `→` キー、ボタン操作でフリップし、往復できます。
- CSS の `transform: rotateY()` のみで実現しており、外部 JavaScript ライブラリは使用していません。
- QR コードの位置には、閲覧中と同じ言語の `/portfolio/` へのリンクを配置しています。
- JavaScript が無効化された環境では、名刺の両面を上下に並べて代替表示します。

### 名刺 SVG の多言語化

- 座標・配色・罫線・アイコン・QR・ロゴは元デザイン（`assets/card-source.svg`）から抽出して引き継ぎ、テキスト要素のみを言語別に再構築しています。元の字詰めは `letter-spacing`（em）で再現しています。
- 印刷用の塗り足しを含んだ座標系のまま、`viewBox` によって仕上がり寸法（55 × 91 mm）を正確に切り出しています。
- 氏名のローマ字表記・SNS アカウント・メールアドレス・QR コードは全言語で共通です。

### フォント

| 用途 | フォント名 | 入手元・ライセンス |
|---|---|---|
| 欧文（名刺・ラベル・コード） | Mona Sans Mono VF | [github/mona-sans](https://github.com/github/mona-sans) 公式 WOFF2 同梱（SIL OFL 1.1） |
| 日本語 / 簡体字中国語 / 韓国語 | Noto Sans JP / SC / KR | Google Fonts より実行時に読み込み |

### 共通仕様

- 言語切り替えドロップダウンは `<details>` 要素をベースに構築。子要素は純粋な `<a href>` リンクであるため、JavaScript 無効環境でも切り替え可能で、検索クローラも巡回できます。
- 各ページに `hreflang`（`x-default` は日本語）、`canonical`、OGP、`html lang` を適切に設定済み。
- ブラウザ言語による自動リダイレクトは行わず、既定は常に日本語としています。
- ライトモード専用設計です。`prefers-reduced-motion`（視覚効果の抑制設定）を尊重します。

## ディレクトリ構成

```
.
├── index.html                # 名刺カード（日本語・既定）
├── en/ · zh/ · ko/           # 名刺カード（各言語版）
├── portfolio/
│   ├── index.html            # ポートフォリオ（日本語）
│   └── en/ · zh/ · ko/       # ポートフォリオ（各言語版）
├── css/
│   ├── tokens.css            # デザイントークン ＋ ベース ＋ 共通コンポーネント
│   ├── card.css              # 名刺カードページ専用スタイル
│   └── portfolio.css         # ポートフォリオページ専用スタイル
├── js/
│   ├── site.js               # 言語ドロップダウン、セクションナビ現在地追従
│   └── card.js               # 3Dフリップ操作（タップ / 左右スワイプ / ←→キー）
├── assets/
│   ├── card/                 # 言語別に生成された名刺面 SVG（front / back）
│   ├── card-source.svg       # 名刺の元デザイン（座標・配色の抽出元）
│   ├── fonts/                # Mona Sans Mono VF ＋ ライセンスファイル
│   ├── goro_logo.svg         # ブランドロゴ
│   └── favicon.ico · og.png · apple-touch-icon.png
├── tools/                    # 静的ページ生成スクリプトとコンテンツ定義
├── 404.html · CNAME · robots.txt · sitemap.xml · .nojekyll
└── LICENSE · LICENSE-CONTENT · THIRD-PARTY-NOTICES.md
```

各ページの HTML および言語別の名刺 SVG は `tools/build.py` により自動生成されます。
**ルート直下の `index.html` などを直接手動編集しても、次回ビルド時に上書きされます。**

## 開発

### 前提環境

- Python 3.13

ページの文言や HTML テンプレートの構築は、Python の標準ライブラリのみで実装されています（外部パッケージのインストールは不要です）。

### ローカル実行

スタイルシートおよびスクリプトをルート絶対パス（`/css/...` 等）で参照しているため、ファイルをブラウザで直接（`file://`）開くと正常に表示されません。必ずローカル HTTP サーバーを介して確認してください。

```bash
python -m http.server 8000
```

起動後、ブラウザで `http://127.0.0.1:8000/` を開きます。

### コンテンツの編集箇所

| 変更したい内容 | 編集対象ファイル |
|---|---|
| 名刺面の氏名・肩書き・所属・キャッチコピー | `tools/content.py` 内の `CARD` 辞書 |
| メールアドレス・SNS・リンク先 URL | `tools/content.py` 内の `CONTACT` 辞書 |
| ボタン・ヒント・meta タグ等の UI 文言 | `tools/content.py` 内の `UI` 辞書 |
| ポートフォリオ本文 | `tools/content_pf/{ja,en,zh,ko}.py` |

### ビルドコマンド

コンテンツを編集後、以下のコマンドで静的ファイル一式を再生成します。

```bash
python tools/build.py          # 全ページ ＋ 404.html ＋ 名刺 SVG ＋ sitemap.xml ＋ robots.txt ＋ CNAME を再生成
```

### 画像の再生成

OGP 画像や favicon を作り直す場合のみ、Pillow を使用します。

```bash
pip install pillow
python tools/make_images.py     # og.png · apple-touch-icon.png · favicon の生成
```

## ドキュメント

| 文書 | 内容 |
|---|---|
| [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md) | 第三者ライセンス表示（Primer Primitives、Mona Sans） |

## ライセンス

本プロジェクトは、対象ごとに **[MIT License](LICENSE)** と **著作権保持（[All Rights Reserved](LICENSE-CONTENT)）** を使い分けて公開しています。

```
Copyright (C) 2026 Gorodrich
```

### 利用条件と特記事項

| 対象 | ライセンス | 該当ファイル |
|---|---|---|
| ソースコード（HTML 構造、`css/`、`js/`、`tools/`） | MIT License | [`LICENSE`](LICENSE) |
| サイト掲載の文章・ロゴ・名刺デザイン・写真等の制作物 | 著作権保持（All Rights Reserved） | [`LICENSE-CONTENT`](LICENSE-CONTENT) |
| 第三者由来アセット（Primer Primitives、フォント） | 各提供元のライセンスを継承 | [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md) |

- **コード再利用時の差し替え注意**：コードをフォークまたは再利用する場合は、掲載文章・`assets/goro_logo.svg`・名刺 SVG・各種個人情報をすべてご自身のものに差し替えてください（これらは MIT License の対象外です）。
- **第三者由来アセット**：`css/tokens.css` のトークン定義値は [primer/primitives](https://github.com/primer/primitives)（MIT, © GitHub, Inc.）を抽出元としています。詳細は [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md) を参照してください。
