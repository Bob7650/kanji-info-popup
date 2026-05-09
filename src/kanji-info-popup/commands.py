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

from aqt import mw
from aqt.utils import tooltip
from . import utils, cache

def make_popup_content(userSelection: str) -> list[str]:
    kanjiList = utils.extract_unique_kanji(userSelection)
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

        if mw.addonManager.getConfig(__name__)["shouldUseAPI"]:
            kanjiData = utils.fetch_kanji_api(kanji)
            if kanjiData:
                print(f"Fetched {kanji} from API")
                cache.save_to_user_cache(kanjiData)
                kanjiDataList.append(kanjiData)
                continue
            print(f"Could not fetch {kanji}")
        else:
            print(f"Can't fetch {kanji}, shouldUseAPI is turned off.")
            tooltip(f"Unknown Kanji {kanji}, shouldUseAPI is turned off in settings.")
    
    displayData = {}
    displayData["kanjiDataList"] = kanjiDataList
    displayData["displayConfig"] = mw.addonManager.getConfig(__name__)["displayConfig"]

    return displayData