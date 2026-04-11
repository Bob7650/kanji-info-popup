import sqlite3
import requests
import json
import time
from typing import List

KANJI_API = "https://kanjiapi.dev/v1/kanji/"

def create_cache_db(db_path: str):
    db = sqlite3.connect(db_path)
    db.execute("""
    CREATE TABLE IF NOT EXISTS kanji_cache (
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
    return db

def fetch_and_store(db, kanji_char: str):
    row = db.execute("SELECT 1 FROM kanji_cache WHERE kanji = ?", kanji_char).fetchone()

    if row: 
        print(f"Skipping {kanji_char}: Kanji already cached")
        return

    try:
        response = requests.get(KANJI_API+kanji_char, timeout=5)
        if response.status_code != 200:
            print(f"Skipping {kanji_char}: HTTP {response.status_code}")
            return
        
        kanji_data = response.json()

        db.execute("""
            INSERT OR REPLACE INTO kanji_cache
            (kanji, meanings, on_readings, kun_readings, heisig_en, grade, jlpt, stroke_count)
            VALUES (?,?,?,?,?,?,?,?)
        """,(
            kanji_data.get("kanji"),
            json.dumps(kanji_data.get("meanings", []), ensure_ascii=False),
            json.dumps(kanji_data.get("on_readings", []), ensure_ascii=False),
            json.dumps(kanji_data.get("kun_readings", []), ensure_ascii=False),
            kanji_data.get("heisig_en"),
            kanji_data.get("grade"),
            kanji_data.get("jlpt"),
            kanji_data.get("stroke_count")
        ))
        db.commit()
        print(f"    Cached: {kanji_char}")
    except requests.RequestException as e:
        print(f"    Error on {kanji_char}: {e}")


def build_cache(kanji_list: List[str], db_path: str = "kanji_cache.db"):
    db = create_cache_db(db_path)
    total = len(kanji_list)

    i = 1
    for char in kanji_list:
        print(f"[{i}/{total}]", end=" ")
        fetch_and_store(db, char)
        time.sleep(0.1)
        i = i+1
    
    db.close()
    print(f"\nDone. DB saved to {db_path}")

def load_joyo_list() -> List[str]:
    response = requests.get("https://raw.githubusercontent.com/davidluzgouveia/kanji-data/master/kanji-jouyou.json", timeout=5)
    data = response.json()
    return list(data.keys())

def main():
    print("Loading Jouyou kanji list...")
    kanji_list = load_joyo_list()
    print(f"Found {len(kanji_list)} kanji.")
    print("Caching...")
    build_cache(kanji_list, db_path="kanji_cache.db")

if __name__ == "__main__":
    main()