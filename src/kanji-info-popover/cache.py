import sqlite3
import requests
import json

from .consts import CACHE_DB_PATH, USER_CACHE_DB_PATH, COLUMNS

def cache_lookup(kanji: str):
    db = sqlite3.connect(CACHE_DB_PATH)
    db.row_factory = sqlite3.Row

    cursor = db.execute(f"SELECT {", ".join(COLUMNS)} FROM kanji_cache WHERE kanji == ?", kanji)
    sqlResult = cursor.fetchone()

    if not sqlResult: return None

    kanjiData = {}
    kanjiData[COLUMNS[0]] = sqlResult[COLUMNS[0]]
    kanjiData[COLUMNS[1]] = json.loads(sqlResult[COLUMNS[1]])
    kanjiData[COLUMNS[2]] = json.loads(sqlResult[COLUMNS[2]])
    kanjiData[COLUMNS[3]] = json.loads(sqlResult[COLUMNS[3]])
    kanjiData[COLUMNS[4]] = sqlResult[COLUMNS[4]]
    kanjiData[COLUMNS[5]] = sqlResult[COLUMNS[5]]
    kanjiData[COLUMNS[6]] = sqlResult[COLUMNS[6]]
    kanjiData[COLUMNS[7]] = sqlResult[COLUMNS[7]]

    return kanjiData

def user_cache_lookup(kanji: str):
    db = sqlite3.connect(USER_CACHE_DB_PATH)
    db.row_factory = sqlite3.Row

    try:
        cursor = db.execute(f"SELECT {", ".join(COLUMNS)} FROM kanji_user_cache WHERE kanji == ?", kanji)
        sqlResult = cursor.fetchone()
    except Exception as e:
        print(f"No user cache exists: {e}")
        return None

    if not sqlResult:
        return None

    kanjiData = {}
    kanjiData[COLUMNS[0]] = sqlResult[COLUMNS[0]]
    kanjiData[COLUMNS[1]] = json.loads(sqlResult[COLUMNS[1]])
    kanjiData[COLUMNS[2]] = json.loads(sqlResult[COLUMNS[2]])
    kanjiData[COLUMNS[3]] = json.loads(sqlResult[COLUMNS[3]])
    kanjiData[COLUMNS[4]] = sqlResult[COLUMNS[4]]
    kanjiData[COLUMNS[5]] = sqlResult[COLUMNS[5]]
    kanjiData[COLUMNS[6]] = sqlResult[COLUMNS[6]]
    kanjiData[COLUMNS[7]] = sqlResult[COLUMNS[7]]

    return kanjiData


def save_to_user_cache(kanjiData: dict):
    try:
        db = sqlite3.connect(USER_CACHE_DB_PATH)
        db.execute("""
        CREATE TABLE IF NOT EXISTS kanji_user_cache (
            kanji TEXT PRIMARY KEY,
            meanings TEXT,
            on_readings TEXT,
            kun_readings TEXT,
            heisig_en TEXT,
            grade INTEGER,
            jlpt INTEGER,
            stroke_count INTEGER,
            fetched_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        db.commit()

        db.execute("""
            INSERT OR REPLACE INTO kanji_user_cache
            (kanji, meanings, on_readings, kun_readings, heisig_en, grade, jlpt, stroke_count)
            VALUES (?,?,?,?,?,?,?,?)
        """,(
            kanjiData["kanji"],
            json.dumps(kanjiData["meanings"], ensure_ascii=False),
            json.dumps(kanjiData["on_readings"], ensure_ascii=False),
            json.dumps(kanjiData["kun_readings"], ensure_ascii=False),
            kanjiData["heisig_en"],
            kanjiData["grade"],
            kanjiData["jlpt"],
            kanjiData["stroke_count"]
        ))
        db.commit()
        print(f"Cached {kanjiData["kanji"]}")
    except requests.RequestException as e:
        print(f"Failed to fetch {kanjiData["kanji"]}: {e}")