import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.filters import load_data, sidebar_filters

# --- PAGE CONFIG ---
st.set_page_config(page_title="Trends Over Time", page_icon="📅", layout="wide")

# --- CUSTOM CSS ---
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
    margin: 45px 0px;
}
.insight-card {
    background-color: white;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    padding: 18px 20px;
    text-align: center;
}
.metric {
    font-size: 28px;
    color: #2E86C1;
    font-weight: 700;
}
.label {
    font-size: 15px;
    color: #616A6B;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("📅 Trends Over Time")
st.caption("Track how startup ecosystems evolved year by year — funding, valuation, success, and growth metrics.")

# --- LOAD & FILTER DATA ---
df = sidebar_filters(load_data())
if df.empty:
    st.warning("⚠️ No data available for the selected filters.")
    st.stop()

# --- PREPROCESS ---
df = df[df["founded_year"].notnull()]
df["founded_year"] = df["founded_year"].astype(int)
yearly = df.groupby("founded_year").agg({
    "funding_musd": "sum",
    "valuation_busd": "mean",
    "success_score": "mean",
    "revenue_musd": "mean"
}).reset_index()

# --- KPIs ---
st.markdown('<p class="section-header">💡 Key Historical Metrics</p>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

total_years = yearly["founded_year"].nunique()
peak_year = yearly.loc[yearly["funding_musd"].idxmax(), "founded_year"]
avg_growth = yearly["funding_musd"].pct_change().mean() * 100

with col1:
    st.markdown(f"<div class='insight-card'><div class='metric'>{total_years}</div><div class='label'>Years of Data</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='insight-card'><div class='metric'>{peak_year}</div><div class='label'>Peak Funding Year</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='insight-card'><div class='metric'>{avg_growth:.2f}%</div><div class='label'>Avg. Annual Funding Growth</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='insight-card'><div class='metric'>{round(yearly['success_score'].mean(),2)}</div><div class='label'>Avg. Global Success Score</div></div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- FUNDING OVER TIME ---
st.markdown('<p class="section-header">💰 Total Funding Over Time</p>', unsafe_allow_html=True)
st.markdown("<p class='subtext'>Compare global funding evolution and see how different countries’ investments have grown across the years.</p>", unsafe_allow_html=True)

# ✨ Adjusted column widths: give more space to Funding by Country
col1, col2 = st.columns([1.2, 2.3])

with col1:
    fig1 = px.area(
        yearly, x="founded_year", y="funding_musd",
        title="🌎 Global Total Funding Over Time",
        color_discrete_sequence=["#2E86C1"]
    )
    fig1.update_layout(
        yaxis_title="Funding ($M)",
        xaxis_title="Year",
        height=400,
        margin=dict(l=10, r=10, t=60, b=40),
        font=dict(size=13)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    trend_country = df.groupby(["founded_year", "country"])["funding_musd"].sum().reset_index()
    fig2 = px.line(
        trend_country, x="founded_year", y="funding_musd",
        color="country", markers=True,
        title="🏆 Funding Growth by Country (Yearly Trend)",
        line_shape="spline"
    )
    fig2.update_traces(line=dict(width=3))
    fig2.update_layout(
        height=600,
        yaxis_title="Funding ($M)",
        xaxis_title="Year",
        legend=dict(orientation="h", y=-0.3),
        margin=dict(l=0, r=0, t=60, b=40),
        font=dict(size=13),
        plot_bgcolor="rgba(255,255,255,1)"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- VALUATION TRENDS ---
st.markdown('<p class="section-header">💎 Valuation Trends Over Time</p>', unsafe_allow_html=True)
st.markdown("<p class='subtext'>Track how startup valuations have evolved globally and identify high-value years.</p>", unsafe_allow_html=True)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=yearly["founded_year"], y=yearly["valuation_busd"],
    mode="lines+markers", name="Valuation ($B)",
    line=dict(color="#16A085", width=4)
))
fig3.add_trace(go.Bar(
    x=yearly["founded_year"], y=yearly["funding_musd"]/1000,
    name="Funding ($B)", marker_color="#AED6F1", opacity=0.5
))
fig3.update_layout(
    title="💎 Valuation vs Funding (Yearly Comparison)",
    xaxis_title="Year",
    yaxis_title="Value",
    legend_title="Metric",
    height=500,
    margin=dict(l=10, r=10, t=60, b=30)
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- SUCCESS TRENDS ---
st.markdown('<p class="section-header">📈 Success Score Evolution</p>', unsafe_allow_html=True)
fig4 = px.line(yearly, x="founded_year", y="success_score", markers=True,
               title="Average Success Score Over Time", color_discrete_sequence=["#F39C12"])
fig4.update_layout(height=450, margin=dict(l=10, r=10, t=50, b=30))
st.plotly_chart(fig4, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- EFFICIENCY OVER TIME ---
st.markdown('<p class="section-header">⚖️ Revenue-to-Valuation Efficiency Trend</p>', unsafe_allow_html=True)
yearly["efficiency_ratio"] = yearly["revenue_musd"] / yearly["valuation_busd"]
fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=yearly["founded_year"], y=yearly["efficiency_ratio"],
    mode="lines+markers", name="Efficiency Ratio",
    line=dict(color="#1ABC9C", width=4)
))
fig5.update_layout(
    title="⚙️ Global Efficiency Ratio (Revenue vs Valuation)",
    xaxis_title="Year", yaxis_title="Efficiency Ratio",
    height=450,
    margin=dict(l=10, r=10, t=60, b=30)
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- INDUSTRY EVOLUTION ---
st.markdown('<p class="section-header">🏭 Industry-Level Funding Evolution</p>', unsafe_allow_html=True)
industry_trend = df.groupby(["founded_year", "industry"])["funding_musd"].sum().reset_index()
fig6 = px.area(industry_trend, x="founded_year", y="funding_musd", color="industry",
               title="Funding Trends by Industry Over Time", groupnorm=None)
fig6.update_layout(height=500, margin=dict(l=10, r=10, t=50, b=30))
st.plotly_chart(fig6, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- GLOBAL FUNDING MAP ---
st.markdown('<p class="section-header">🌍 Global Funding Map (Over the Years)</p>', unsafe_allow_html=True)
map_data = df.groupby(["country", "founded_year"])["funding_musd"].sum().reset_index()
fig7 = px.choropleth(
    map_data, locations="country", locationmode="country names",
    color="funding_musd", hover_name="country",
    animation_frame="founded_year", color_continuous_scale="Viridis",
    title="Yearly Global Funding Distribution"
)
fig7.update_layout(height=550, margin=dict(l=0, r=0, t=60, b=30))
st.plotly_chart(fig7, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- SUMMARY INSIGHTS ---
st.subheader("🧠 Insights & Observations")

peak_funding = yearly.loc[yearly["funding_musd"].idxmax()]
peak_success = yearly.loc[yearly["success_score"].idxmax()]
decline = yearly["funding_musd"].pct_change().iloc[-1] * 100

st.markdown(f"""
- 💸 **{int(peak_funding['founded_year'])}** marked the **highest global funding** (~${round(peak_funding['funding_musd'],2)}M).
- 💎 Valuation and funding moved **closely correlated**, showing consistent growth patterns.
- 🚀 Success scores peaked around **{int(peak_success['founded_year'])}**, reflecting optimized ecosystem maturity.
- ⚙️ Efficiency improved steadily but plateaued after peak funding years — possibly due to scaling inefficiencies.
- 🌍 Overall CAGR: **{round(avg_growth,2)}%**, with a mild recent contraction of **{round(decline,2)}%**, suggesting market stabilization.
""")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
