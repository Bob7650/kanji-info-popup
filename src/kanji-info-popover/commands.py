from . import utils
from .cache import cache

def make_popup_content(userSelection: str) -> list[str]:
    kanjiList = utils.extract_kanji(userSelection)
    kanjiDataList = []

    if len(kanjiList) == 0:
        print("No kanji inside selection")
        return kanjiDataList
    
    for kanji in kanjiList:
        kanjiData = cache.cache_lookup(kanji)
        if kanjiData:
            print(f"Found {kanji} in cache")
            kanjiDataList.append(kanjiData)
            continue
        print(f"Could not find {kanji} in cache")
        
        kanjiData = cache.user_cache_lookup(kanji)
        if kanjiData: 
            print(f"Found {kanji} in user cache")
            kanjiDataList.append(kanjiData)
            continue
        print(f"Could not find {kanji} in user cache")

        kanjiData = utils.fetch_kanji_api(kanji)
        if kanjiData:
            print(f"Fetched {kanji} from API")
            cache.save_to_user_cache(kanjiData)
            kanjiDataList.append(kanjiData)
            continue
        print(f"Could not fetch {kanji}")
    
    return kanjiDataList