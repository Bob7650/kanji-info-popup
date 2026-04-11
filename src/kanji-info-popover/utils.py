import requests
from typing import Any
from .const import KANJI_API

#remove duplicates
def extract_kanji(text: str) -> list[str]:
    # CJK Unified Ideographs block: U+4E00–U+9FFF
    return [ch for ch in text if '\u4e00' <= ch <= '\u9fff']

#think about doing this on another thread and maybe cooldown between requests
def fetch_kanji_api(kanji: str) -> Any:
    response = requests.get(KANJI_API+kanji, timeout=5)

    if response.status_code != 200:
        return None
    
    return response.json()