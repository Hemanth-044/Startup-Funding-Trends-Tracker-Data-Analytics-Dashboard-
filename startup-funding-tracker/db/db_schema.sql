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
CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS analytics (day DATE PRIMARY KEY, visits INTEGER DEFAULT 0);
