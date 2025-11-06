import sqlite3
import pandas as pd
from pathlib import Path

DB = Path("db/funding.db")
INTERIM = Path("data/interim")

con = sqlite3.connect(DB)
cur = con.cursor()

schema = """
CREATE TABLE IF NOT EXISTS startups (
    startup_id TEXT PRIMARY KEY,
    name TEXT,
    founded_year INTEGER,
    country TEXT,
    industry TEXT,
    funding_stage TEXT,
    funding_musd REAL,
    employees INTEGER,
    revenue_musd REAL,
    valuation_busd REAL,
    success_score REAL,
    acquired INTEGER,
    ipo INTEGER,
    customers_mil REAL,
    tech_stack TEXT,
    followers REAL
);
"""
cur.executescript(schema)

df = pd.read_csv(INTERIM / "startups_clean.csv")
df.to_sql("startups", con, if_exists="replace", index=False)

cur.execute("""
CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")
cur.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES ('last_updated', datetime('now'))")

con.commit()
con.close()
print("✅ Data successfully loaded into db/funding.db")
