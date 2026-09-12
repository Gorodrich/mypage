# -*- coding: utf-8 -*-
"""
サイト全体のテキストコンテンツ。
ここを書き換えて `python tools/build.py` を実行すると、全 8 ページと
名刺 SVG (assets/card/*.svg) が再生成されます。

翻訳は機械翻訳ではなく、各言語ごとに個別に書き起こしたテキストです。
本人の原稿ができたら、この 1 ファイルを差し替えるだけで反映されます。
"""

SITE = {
    "domain": "56dri.ch",
    "origin": "https://56dri.ch",
    # フッターのライセンスリンク先。GitHub Pages は拡張子なしファイルと .md を
    # ダウンロード扱いにするため、リポジトリ側の整形表示へ飛ばす
    "repo_blob": "https://github.com/Gorodrich/mypage/blob/main",
}

LANGS = ["ja", "en", "zh", "ko"]

# html lang 属性 / hreflang / ドロップダウンの表示名
LANG_META = {
    "ja": {"html": "ja",      "hreflang": "ja",      "label": "日本語",  "card_prefix": "",     "pf_prefix": ""},
    "en": {"html": "en",      "hreflang": "en",      "label": "English", "card_prefix": "en/",  "pf_prefix": "en/"},
    "zh": {"html": "zh-Hans", "hreflang": "zh-Hans", "label": "中文",    "card_prefix": "zh/",  "pf_prefix": "zh/"},
    "ko": {"html": "ko",      "hreflang": "ko",      "label": "한국어",  "card_prefix": "ko/",  "pf_prefix": "ko/"},
}

# SVG 内で使う CJK フォントスタック(言語ごと)
CJK_STACK = {
    "ja": '"Noto Sans JP","Hiragino Sans","Yu Gothic",sans-serif',
    "en": '"Noto Sans JP","Hiragino Sans","Yu Gothic",sans-serif',
    "zh": '"Noto Sans SC","Noto Sans JP","PingFang SC","Microsoft YaHei",sans-serif',
    "ko": '"Noto Sans KR","Noto Sans JP","Apple SD Gothic Neo","Malgun Gothic",sans-serif',
}

# ---------------------------------------------------------------------------
# 言語によって変わらない固有名詞(氏名ローマ字・SNS ID・URL)
# ---------------------------------------------------------------------------
CONTACT = {
    "email":  {"id": "mail@56dri.ch", "href": "mailto:mail@56dri.ch"},
    "github": {"id": "gorodrich",     "href": "https://github.com/gorodrich"},
    "x":      {"id": "56drich",       "href": "https://x.com/56drich"},
    "note":   {"id": "56drich",       "href": "https://note.com/56drich"},
    "zenn":   {"id": "56drich",       "href": "https://zenn.dev/56drich"},
}
WORDMARK = "GORODRICH"
SITE_URL_LABEL = "https://56dri.ch"

# ---------------------------------------------------------------------------
# 名刺面の言語依存テキスト
#   font: "mono" = Mona Sans Mono VF / "cjk" = Noto Sans JP|SC|KR
# ---------------------------------------------------------------------------
CARD = {
    "ja": {
        "name_main": {"text": "ゴロードリヒ", "font": "cjk",  "size": 6.2, "weight": 600, "ls": 0},
        "name_sub":  {"text": "GORODRICH",   "font": "mono", "size": 2.5, "weight": 400, "ls": 0.219},
        "title": [
            {"text": "法学徒 ×",           "font": "cjk", "size": 2.4, "weight": 500},
            {"text": "インフラエンジニア", "font": "cjk", "size": 2.4, "weight": 500},
        ],
        "affiliation": {"text": "中央大学 法学部 法律学科", "font": "cjk", "size": 2.7, "weight": 400},
        "tagline":     {"text": "昼法夜鯖 - 昼は法律、夜は鯖缶", "font": "cjk", "size": 2.0, "weight": 400, "ls": 0.02},
    },
    "en": {
        "name_main": {"text": "GORODRICH",     "font": "mono", "size": 5.0, "weight": 600, "ls": 0.06},
        "name_sub":  {"text": "ゴロードリヒ",   "font": "cjk",  "size": 2.5, "weight": 400, "ls": 0.02},
        "title": [
            {"text": "Law Student ×",           "font": "mono", "size": 2.3, "weight": 500},
            {"text": "Infrastructure Engineer", "font": "mono", "size": 2.3, "weight": 500},
        ],
        "affiliation": {"text": "Chuo University, Faculty of Law", "font": "mono", "size": 2.3, "weight": 400},
        "tagline":     {"text": "Law by Day, Ops by Night", "font": "mono", "size": 2.2, "weight": 400, "ls": 0},
    },
    "zh": {
        "name_main": {"text": "五郎德里希",  "font": "cjk",  "size": 6.2, "weight": 600, "ls": 0},
        "name_sub":  {"text": "GORODRICH", "font": "mono", "size": 2.5, "weight": 400, "ls": 0.219},
        "title": [
            {"text": "法学院学生 ×",   "font": "cjk", "size": 2.4, "weight": 500},
            {"text": "基础架构工程师", "font": "cjk", "size": 2.4, "weight": 500},
        ],
        "affiliation": {"text": "中央大学 法学院 法律学系", "font": "cjk", "size": 2.7, "weight": 400},
        "tagline":     {"text": "昼法夜维 - 白天学法，晚上运维", "font": "cjk", "size": 2.0, "weight": 400, "ls": 0.02},
    },
    "ko": {
        "name_main": {"text": "고로드리히", "font": "cjk",  "size": 6.0, "weight": 600, "ls": 0},
        "name_sub":  {"text": "GORODRICH", "font": "mono", "size": 2.5, "weight": 400, "ls": 0.219},
        "title": [
            {"text": "법학도 ×",        "font": "cjk", "size": 2.4, "weight": 500},
            {"text": "인프라 엔지니어", "font": "cjk", "size": 2.4, "weight": 500},
        ],
        "affiliation": {"text": "주오대학 법학부 법률학과", "font": "cjk", "size": 2.5, "weight": 400},
        "tagline":     {"text": "낮에는 법학도, 밤에는 서버장", "font": "cjk", "size": 2.2, "weight": 400, "ls": 0.01},
    },
}


# ---------------------------------------------------------------------------
# UI 文言(ナビゲーション・ボタン・メタ情報)
# ---------------------------------------------------------------------------
UI = {
    "ja": {
        "card_title": "ゴロードリヒ | デジタル名刺",
        "card_desc": "中央大学 法学部の法学生 兼 インフラエンジニア、ゴロードリヒのデジタル名刺。連絡先とポートフォリオはこちらから。",
        "pf_title": "ポートフォリオ | ゴロードリヒ",
        "pf_desc": "ゴロードリヒのポートフォリオ。自己紹介・経歴・スキル・実績をまとめています。",
        "lang_menu": "言語",
        "lang_current": "表示中の言語",
        "flip_to_info": "情報面を見る",
        "flip_to_logo": "ロゴ面に戻る",
        "hint": "カードをタップ、または左右にスワイプすると裏返ります",
        "face_logo": "名刺 ロゴ面",
        "face_info": "名刺 情報面",
        "portfolio_cta": "ポートフォリオを見る",
        "qr_label": "ポートフォリオページを開く",
        "email_label": "メールを送る",
        "back_to_card": "名刺に戻る",
        "pf_kicker": "PORTFOLIO",
        "pf_lead": "昼法夜鯖 - 昼は法律、夜は鯖缶。",
        "toc": "目次",
        "skill_level": "習熟度",
        "top": "ページ先頭へ",
        "footer_note": "このサイトはコードとコンテンツで異なるライセンスを採用するデュアルライセンス構成です。",
        "lic_code": "コード: MIT",
        "lic_content": "文章・デザイン: 無断転載禁止",
        "lic_third": "サードパーティ表記",
        "period": "期間",
        "role": "役割",
        "stack": "使用技術",
        "notfound_heading": "ページが見つかりません",
        "notfound_body": "お探しのページは移動または削除された可能性があります。",
        "notfound_home": "ホームに戻る",
    },
    "en": {
        "card_title": "GORODRICH | Digital Business Card",
        "card_desc": "Digital business card of Gorodrich — law student at Chuo University and infrastructure engineer. Contact details and portfolio.",
        "pf_title": "Portfolio | GORODRICH",
        "pf_desc": "Portfolio of Gorodrich: about me, career history, skills and selected work.",
        "lang_menu": "Language",
        "lang_current": "Current language",
        "flip_to_info": "Show contact side",
        "flip_to_logo": "Back to logo side",
        "hint": "Tap the card or swipe sideways to flip it",
        "face_logo": "Business card, logo side",
        "face_info": "Business card, contact side",
        "portfolio_cta": "View portfolio",
        "qr_label": "Open the portfolio page",
        "email_label": "Send an email",
        "back_to_card": "Back to the card",
        "pf_kicker": "PORTFOLIO",
        "pf_lead": "Law by day, operations by night.",
        "toc": "Contents",
        "skill_level": "Proficiency",
        "top": "Back to top",
        "footer_note": "This site is dual-licensed: the source code and the site content are released under different terms.",
        "lic_code": "Code: MIT",
        "lic_content": "Content: all rights reserved",
        "lic_third": "Third-party notices",
        "period": "Period",
        "role": "Role",
        "stack": "Stack",
        "notfound_heading": "Page not found",
        "notfound_body": "The page you're looking for may have been moved or removed.",
        "notfound_home": "Back to home",
    },
    "zh": {
        "card_title": "五郎德里希 | 电子名片",
        "card_desc": "中央大学法学院学生兼基础架构工程师五郎德里希的电子名片。可在此查看联系方式与作品集。",
        "pf_title": "作品集 | 五郎德里希",
        "pf_desc": "五郎德里希的作品集，收录自我介绍、履历、技能与项目实绩。",
        "lang_menu": "语言",
        "lang_current": "当前语言",
        "flip_to_info": "查看信息面",
        "flip_to_logo": "返回标志面",
        "hint": "点按名片或左右滑动即可翻面",
        "face_logo": "名片 标志面",
        "face_info": "名片 信息面",
        "portfolio_cta": "查看作品集",
        "qr_label": "打开作品集页面",
        "email_label": "发送邮件",
        "back_to_card": "返回名片",
        "pf_kicker": "PORTFOLIO",
        "pf_lead": "昼法夜维 - 白天学法，晚上运维。",
        "toc": "目录",
        "skill_level": "熟练度",
        "top": "回到顶部",
        "footer_note": "本站采用双重许可:源代码与网站内容适用不同的授权条款。",
        "lic_code": "代码:MIT",
        "lic_content": "内容:保留所有权利",
        "lic_third": "第三方声明",
        "period": "期间",
        "role": "角色",
        "stack": "技术栈",
        "notfound_heading": "页面未找到",
        "notfound_body": "您要访问的页面可能已被移动或删除。",
        "notfound_home": "返回首页",
    },
    "ko": {
        "card_title": "고로드리히 | 디지털 명함",
        "card_desc": "주오대학 법학부 재학생이자 인프라 엔지니어인 고로드리히의 디지털 명함. 연락처와 포트폴리오를 확인하세요.",
        "pf_title": "포트폴리오 | 고로드리히",
        "pf_desc": "고로드리히의 포트폴리오. 자기소개, 경력, 기술 스택, 작업물을 정리했습니다.",
        "lang_menu": "언어",
        "lang_current": "현재 언어",
        "flip_to_info": "정보 면 보기",
        "flip_to_logo": "로고 면으로 돌아가기",
        "hint": "카드를 탭하거나 좌우로 스와이프하면 뒤집힙니다",
        "face_logo": "명함 로고 면",
        "face_info": "명함 정보 면",
        "portfolio_cta": "포트폴리오 보기",
        "qr_label": "포트폴리오 페이지 열기",
        "email_label": "메일 보내기",
        "back_to_card": "명함으로 돌아가기",
        "pf_kicker": "PORTFOLIO",
        "pf_lead": "낮에는 법학도, 밤에는 서버장.",
        "toc": "목차",
        "skill_level": "숙련도",
        "top": "맨 위로",
        "footer_note": "이 사이트는 소스 코드와 사이트 콘텐츠에 서로 다른 라이선스를 적용하는 듀얼 라이선스 구성입니다.",
        "lic_code": "코드: MIT",
        "lic_content": "콘텐츠: 모든 권리 보유",
        "lic_third": "서드파티 고지",
        "period": "기간",
        "role": "역할",
        "stack": "기술",
        "notfound_heading": "페이지를 찾을 수 없습니다",
        "notfound_body": "찾으시는 페이지가 이동되었거나 삭제되었을 수 있습니다.",
        "notfound_home": "홈으로 돌아가기",
    },
}
