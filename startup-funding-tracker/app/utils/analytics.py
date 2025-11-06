# app/utils/analytics.py
import datetime
from .db import get_conn
import pandas as pd

def bump_visit():
    """Increment daily visitor count."""
    con = get_conn()
    today = datetime.date.today().isoformat()
    con.execute(
        "INSERT INTO analytics(day, visits) VALUES(?,1) "
        "ON CONFLICT(day) DO UPDATE SET visits = visits + 1",
        (today,)
    )
    con.commit()

def get_visit_trend():
    """Fetch historical daily visits."""
    return pd.read_sql("SELECT day, visits FROM analytics ORDER BY day", get_conn())

def total_visits():
    """Get total lifetime visits."""
    df = pd.read_sql("SELECT SUM(visits) AS total FROM analytics", get_conn())
    return int(df['total'][0]) if not df.empty else 0
