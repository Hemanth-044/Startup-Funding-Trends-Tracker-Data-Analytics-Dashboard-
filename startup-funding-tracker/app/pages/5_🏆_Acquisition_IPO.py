import streamlit as st
from utils import queries

st.title("🏆 Acquisition & IPO Insights")

data = queries.acquisition_ipo_stats()
acq_rate = (data['total_acquired'] / data['total_startups']) * 100
ipo_rate = (data['total_ipo'] / data['total_startups']) * 100

st.metric("🏢 % Acquired Startups", f"{acq_rate:.1f}%")
st.metric("📈 % IPO Startups", f"{ipo_rate:.1f}%")
