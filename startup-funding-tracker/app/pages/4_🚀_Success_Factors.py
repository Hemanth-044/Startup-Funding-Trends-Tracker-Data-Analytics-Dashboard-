import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.filters import load_data, sidebar_filters
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Success Factors", page_icon="🚀", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
<style>
.section-header {
    font-size: 28px;
    color: #1A5276;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 15px;
    border-left: 5px solid #2E86C1;
    padding-left: 12px;
}
.subtext {
    color: #626567;
    font-size: 15px;
    margin-bottom: 12px;
}
.divider {
    border-top: 2px solid #E5E8E8;
    margin: 40px 0px;
}
.insight-box {
    background: linear-gradient(135deg, #E8F8F5, #EBF5FB);
    border-radius: 12px;
    padding: 18px 22px;
    font-size: 15px;
    color: #154360;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🚀 Startup Success Factors")
st.caption("Discover what drives startup success — from funding and valuation to team size and market reach.")

# --- LOAD DATA ---
df = sidebar_filters(load_data())
if df.empty:
    st.warning("⚠️ No data available for the selected filters.")
    st.stop()

# --- DATA PREP ---
numeric_cols = ["funding_musd", "valuation_busd", "revenue_musd", "employees", "success_score", "customers_mil", "followers"]
data = df[numeric_cols].dropna()

st.markdown('<p class="section-header">📊 Correlation Between Metrics</p>', unsafe_allow_html=True)
st.markdown("<p class='subtext'>Understand how different metrics relate to startup success using correlation heatmaps.</p>", unsafe_allow_html=True)

# --- CORRELATION HEATMAP ---
corr = data.corr()
fig_corr = px.imshow(
    corr, text_auto=True, color_continuous_scale="Blues",
    title="Correlation Matrix of Key Metrics", aspect="auto"
)
fig_corr.update_layout(height=600, margin=dict(l=0, r=0, t=60, b=40))
st.plotly_chart(fig_corr, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- FEATURE IMPORTANCE (SIMULATED ML INSIGHT) ---
st.markdown('<p class="section-header">⚖️ Most Influential Factors Driving Success</p>', unsafe_allow_html=True)
st.markdown("<p class='subtext'>Ranking of features that correlate most strongly with startup success scores.</p>", unsafe_allow_html=True)

# Compute simple feature importance (absolute correlation with success_score)
importance = corr["success_score"].drop("success_score").abs().sort_values(ascending=False).reset_index()
importance.columns = ["Feature", "Importance"]

fig_imp = px.bar(
    importance, x="Importance", y="Feature", orientation="h",
    color="Importance", color_continuous_scale="Tealgrn",
    title="Top Factors Influencing Success Score"
)
fig_imp.update_layout(height=500, margin=dict(l=10, r=10, t=60, b=40))
st.plotly_chart(fig_imp, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- SUCCESS VS FUNDING ---
st.markdown('<p class="section-header">💰 Funding vs Success</p>', unsafe_allow_html=True)
st.markdown("<p class='subtext'>Do higher-funded startups perform better? Explore the relationship between funding and success score.</p>", unsafe_allow_html=True)

fig_fund = px.scatter(
    df, x="funding_musd", y="success_score", size="valuation_busd", color="industry",
    hover_name="industry", title="Funding vs Success (Bubble Size = Valuation $B)"
)
fig_fund.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
fig_fund.update_layout(height=500, margin=dict(l=10, r=10, t=60, b=40))
st.plotly_chart(fig_fund, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- SUCCESS VS EMPLOYEES ---
st.markdown('<p class="section-header">👥 Employees vs Success</p>', unsafe_allow_html=True)
st.markdown("<p class='subtext'>Is there an optimal team size for success? This chart shows how the number of employees impacts performance.</p>", unsafe_allow_html=True)

fig_emp = px.scatter(
    df, x="employees", y="success_score", color="industry", trendline="ols",
    title="Employee Count vs Success Score by Industry"
)
fig_emp.update_layout(height=500, margin=dict(l=10, r=10, t=60, b=40))
st.plotly_chart(fig_emp, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- SUCCESS VS VALUATION ---
st.markdown('<p class="section-header">💎 Valuation vs Success Over Time</p>', unsafe_allow_html=True)
yearly = df.groupby("founded_year")[["valuation_busd", "success_score"]].mean().reset_index()
fig_val = go.Figure()
fig_val.add_trace(go.Scatter(
    x=yearly["founded_year"], y=yearly["success_score"],
    mode="lines+markers", name="Success Score", line=dict(color="#F39C12", width=3)
))
fig_val.add_trace(go.Scatter(
    x=yearly["founded_year"], y=yearly["valuation_busd"] * 10,
    mode="lines+markers", name="Valuation (scaled ×10)", line=dict(color="#1ABC9C", width=3, dash="dot")
))
fig_val.update_layout(
    title="Success Score vs Valuation Over Time",
    xaxis_title="Year",
    yaxis_title="Success / Valuation (scaled)",
    height=500,
    margin=dict(l=10, r=10, t=60, b=40)
)
st.plotly_chart(fig_val, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- INDUSTRY-WISE SUCCESS ---
st.markdown('<p class="section-header">🏭 Average Success by Industry</p>', unsafe_allow_html=True)
st.markdown("<p class='subtext'>Identify which sectors consistently produce successful startups.</p>", unsafe_allow_html=True)

industry_success = df.groupby("industry")["success_score"].mean().sort_values(ascending=True).reset_index()
fig_ind = px.bar(
    industry_success, x="success_score", y="industry",
    orientation="h", color="success_score", color_continuous_scale="Blues",
    title="Average Success Score by Industry"
)
fig_ind.update_layout(height=500, margin=dict(l=10, r=10, t=60, b=40))
st.plotly_chart(fig_ind, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- INSIGHT SUMMARY ---
st.markdown('<p class="section-header">🧠 Insights & Observations</p>', unsafe_allow_html=True)

top_factor = importance.iloc[0]["Feature"]
second_factor = importance.iloc[1]["Feature"]
lowest_factor = importance.iloc[-1]["Feature"]
top_industry = industry_success.iloc[-1]["industry"]

st.markdown(f"""
<div class='insight-box'>
<b>Key Insights:</b><br><br>
✅ The most influential factor for startup success is <b>{top_factor.replace('_', ' ').title()}</b>, 
closely followed by <b>{second_factor.replace('_', ' ').title()}</b>.<br>
💡 <b>{top_industry}</b> startups lead in average success scores across all industries.<br>
⚖️ Startups with balanced <b>funding-to-valuation ratios</b> tend to perform better in long-term growth.<br>
👥 There’s a visible saturation point — beyond a certain employee count, <b>success scores plateau</b>.<br>
📉 <b>{lowest_factor.replace('_', ' ').title()}</b> shows the weakest direct correlation to success, 
suggesting limited influence or indirect impact.<br>
</div>
""", unsafe_allow_html=True)
