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
