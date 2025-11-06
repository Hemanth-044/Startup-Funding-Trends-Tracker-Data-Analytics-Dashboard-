import streamlit as st
import pandas as pd
from utils.db import get_conn

@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM startups", get_conn())

def sidebar_filters(df):
    st.sidebar.header("🔍 Filters")

    countries = sorted(df['country'].dropna().unique().tolist())
    industries = sorted(df['industry'].dropna().unique().tolist())
    years = sorted(df['founded_year'].dropna().unique().astype(int).tolist())

    selected_country = st.sidebar.multiselect("🌍 Country", countries, default=countries[:3])
    selected_industry = st.sidebar.multiselect("🏭 Industry", industries, default=industries[:5])
    selected_year = st.sidebar.slider("📅 Founded Year", min(years), max(years), (min(years), max(years)))

    filtered_df = df[
        (df['country'].isin(selected_country)) &
        (df['industry'].isin(selected_industry)) &
        (df['founded_year'].between(*selected_year))
    ]
    return filtered_df
