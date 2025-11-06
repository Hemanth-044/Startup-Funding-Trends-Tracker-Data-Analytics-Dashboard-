import sqlite3
from functools import lru_cache

DB_PATH = "db/funding.db"

@lru_cache(maxsize=1)
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)
