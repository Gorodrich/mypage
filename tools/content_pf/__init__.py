# -*- coding: utf-8 -*-
"""言語別ポートフォリオ本文。ja/en/zh/ko の各モジュールを束ねる。"""
from . import ja, en, zh, ko

PORTFOLIO = {"ja": ja.DATA, "en": en.DATA, "zh": zh.DATA, "ko": ko.DATA}
