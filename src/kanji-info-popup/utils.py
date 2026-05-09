# Copyright (C) 2026 Hubert Drążek
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import requests
from typing import Any
from .consts import KANJI_API

def extract_unique_kanji(text: str) -> list[str]:
    # CJK Unified Ideographs block: U+4E00–U+9FFF
    kanjiList = []
    for ch in text:
        if not ('\u4e00' <= ch <= '\u9fff'):
            #not a kanji
            continue
        if ch in kanjiList:
            #duplicate
            continue
        kanjiList.append(ch)

    return kanjiList

#think about doing this on another thread and maybe cooldown between requests
def fetch_kanji_api(kanji: str) -> Any:
    response = requests.get(KANJI_API+kanji, timeout=5)

    if response.status_code != 200:
        return None
    
    return response.json()
