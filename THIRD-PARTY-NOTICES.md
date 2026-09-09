# Third-Party Notices

This site incorporates or depends on the following third-party material. Each
item remains under its own license; the licenses below take precedence over
this repository's `LICENSE` and `LICENSE-CONTENT` for the material they cover.

---

## 1. Primer Primitives (design tokens) — MIT

- Source: https://github.com/primer/primitives
- Copyright (c) GitHub, Inc.
- Used for: the design-token values in `css/tokens.css` (colour, typography,
  spacing, radius, shadow, motion). The values were extracted from Primer
  Primitives' token source; the CSS file itself is authored for this project.

```
MIT License

Copyright (c) GitHub, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

> Note: the working notes under `GitHub Primer Design System/` (a summary of
> Primer generated with Claude Design) are a build-time reference only and are
> excluded from the published repository via `.gitignore`.

---

## 2. Mona Sans Mono — SIL Open Font License 1.1

- Source: https://github.com/github/mona-sans
- Copyright (c) 2023, GitHub, with Reserved Font Name "Mona Sans"
- Bundled file: `assets/fonts/MonaSansMonoVF.woff2`
- Full license text: `assets/fonts/MONA-SANS-OFL.txt`

The font is used as a web font under the OFL. It is not sold, and no
derivative renamed with the reserved font name is distributed.

---

## 3. Noto Sans JP / Noto Sans SC / Noto Sans KR — SIL Open Font License 1.1

- Copyright (c) The Noto Project Authors (https://github.com/notofonts)
- Loaded at runtime from Google Fonts (`fonts.googleapis.com` /
  `fonts.gstatic.com`); not redistributed in this repository.
- License: https://openfontlicense.org

---

## 4. Fallback system fonts

The CSS also references common system fonts (e.g. system-ui and platform
defaults) by name only. No font files for these are included or distributed.
