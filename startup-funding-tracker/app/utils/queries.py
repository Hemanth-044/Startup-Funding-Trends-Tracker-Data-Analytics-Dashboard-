import pandas as pd
from .db import get_conn

def kpis():
    q = "SELECT SUM(funding_musd) AS total_funding, AVG(valuation_busd) AS avg_valuation, AVG(success_score) AS avg_success FROM startups"
    return pd.read_sql(q, get_conn()).iloc[0].to_dict()

def top_industries():
    q = "SELECT industry, SUM(funding_musd) AS total FROM startups GROUP BY industry ORDER BY total DESC LIMIT 10"
    return pd.read_sql(q, get_conn())

def top_countries():
    q = "SELECT country, SUM(funding_musd) AS total FROM startups GROUP BY country ORDER BY total DESC LIMIT 10"
    return pd.read_sql(q, get_conn())

def funding_vs_valuation():
    q = "SELECT funding_musd, valuation_busd, industry FROM startups WHERE funding_musd IS NOT NULL AND valuation_busd IS NOT NULL"
    return pd.read_sql(q, get_conn())

def acquisition_ipo_stats():
    q = """
    SELECT 
        SUM(acquired) AS total_acquired,
        SUM(ipo) AS total_ipo,
        COUNT(*) AS total_startups
    FROM startups
    """
    return pd.read_sql(q, get_conn()).iloc[0].to_dict()
