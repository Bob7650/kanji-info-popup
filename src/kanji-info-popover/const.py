import os

CACHE_DB_PATH = os.path.join(os.path.dirname(__file__), "cache/kanji_mini_cache.db")
USER_CACHE_DB_PATH = os.path.join(os.path.dirname(__file__), "cache/kanji_user_cache.db")
COLUMNS = ["kanji", "meanings", "on_readings", "kun_readings", "heisig_en", "grade", "jlpt", "stroke_count"]
KANJI_API = "https://kanjiapi.dev/v1/kanji/"