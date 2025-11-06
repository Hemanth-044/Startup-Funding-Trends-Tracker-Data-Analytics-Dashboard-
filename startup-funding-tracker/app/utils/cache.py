import streamlit as st
from datetime import timedelta
from . import queries

@st.cache_data(ttl=timedelta(hours=6))
def cached_industry_data():
    """Cache top industry data for 6 hours."""
    return queries.top_industries()

@st.cache_data(ttl=timedelta(hours=6))
def cached_country_data():
    """Cache top country data for 6 hours."""
    return queries.top_countries()

def clear_cache():
    st.cache_data.clear()
    st.success("✅ Cache cleared — data will refresh next time.")
