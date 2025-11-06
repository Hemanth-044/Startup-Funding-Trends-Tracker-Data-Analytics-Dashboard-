import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.filters import load_data, sidebar_filters

# --- PAGE CONFIG ---
st.set_page_config(page_title="Country Insights", page_icon="🌍", layout="wide")

# --- CUSTOM STYLES ---
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
    font-size: 14px;
    margin-bottom: 10px;
}
.insight-card {
    background-color: white;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    padding: 18px 20px;
    margin-bottom: 10px;
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
.divider {
    border-top: 2px solid #E5E8E8;
    margin: 35px 0px;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🌍 Country Insights")
st.caption("Discover how countries differ in funding strength, valuation, success, and efficiency — backed by data-driven insights.")

# --- LOAD & FILTER DATA ---
df = sidebar_filters(load_data())
if df.empty:
    st.warning("⚠️ No data available for selected filters.")
    st.stop()

# --- KPI CARDS ---
st.markdown('<p class="section-header">💡 Global Overview</p>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

top_fund_country = df.groupby("country")["funding_musd"].sum().idxmax()
top_val_country = df.groupby("country")["valuation_busd"].mean().idxmax()
avg_success = round(df["success_score"].mean(), 2)
total_funding = round(df["funding_musd"].sum(), 2)

with col1:
    st.markdown(f"<div class='insight-card'><div class='metric'>{df['country'].nunique()}</div><div class='label'>Countries Analyzed</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='insight-card'><div class='metric'>{top_fund_country}</div><div class='label'>Top Funded Country</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='insight-card'><div class='metric'>{top_val_country}</div><div class='label'>Highest Valuation</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='insight-card'><div class='metric'>{avg_success}</div><div class='label'>Avg. Global Success Score</div></div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- COUNTRY SELECTION ---
countries = sorted(df["country"].unique())
selected_countries = st.multiselect("🌎 Compare Specific Countries", countries, default=countries[:6])
filtered_df = df[df["country"].isin(selected_countries)]

if filtered_df.empty:
    st.warning("No data for selected countries.")
    st.stop()

# --- FUNDING DISTRIBUTION ---
st.markdown('<p class="section-header">💰 Total Funding & Growth</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    fund_data = filtered_df.groupby("country")["funding_musd"].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(fund_data, x="funding_musd", y="country", orientation="h",
                 color="funding_musd", color_continuous_scale="Blues",
                 title="Total Startup Funding by Country ($M)", text_auto=".2s")
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    yearly = filtered_df.groupby(["founded_year", "country"])["funding_musd"].sum().reset_index()
    fig2 = px.area(yearly, x="founded_year", y="funding_musd", color="country",
                   title="Funding Growth Over Time", line_group="country")
    fig2.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- VALUATION vs SUCCESS ---
st.markdown('<p class="section-header">💎 Valuation vs Success Performance</p>', unsafe_allow_html=True)
corr = filtered_df.groupby("country")[["valuation_busd", "success_score"]].mean().reset_index()
fig3 = px.scatter(corr, x="valuation_busd", y="success_score",
                  size="valuation_busd", color="country", hover_name="country",
                  title="Valuation vs Success Score (Avg per Country)")
st.plotly_chart(fig3, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- EFFICIENCY MATRIX ---
st.markdown('<p class="section-header">⚖️ Revenue Efficiency Matrix</p>', unsafe_allow_html=True)
eff = filtered_df.groupby("country")[["revenue_musd", "valuation_busd", "employees"]].mean().reset_index()
eff["efficiency"] = eff["revenue_musd"] / eff["valuation_busd"]
fig4 = px.scatter(eff, x="employees", y="efficiency", size="valuation_busd", color="country",
                  hover_name="country", title="Revenue-to-Valuation Efficiency vs Employees")
st.plotly_chart(fig4, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- GEO FUNDING MAP ---
st.markdown('<p class="section-header">🌍 Global Funding Map</p>', unsafe_allow_html=True)
geo = df.groupby("country")["funding_musd"].sum().reset_index()
fig5 = px.choropleth(
    geo, locations="country", locationmode="country names",
    color="funding_musd", hover_name="country",
    color_continuous_scale="Viridis",
    title="Global Distribution of Startup Funding ($M)"
)
fig5.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))
st.plotly_chart(fig5, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- RADAR CHART (MULTI-METRIC COMPARISON) ---
st.markdown('<p class="section-header">📊 Multi-Metric Comparison (Radar View)</p>', unsafe_allow_html=True)
metric_cols = ["funding_musd", "valuation_busd", "success_score", "revenue_musd", "employees"]
radar_data = filtered_df.groupby("country")[metric_cols].mean().reset_index()
radar_data_norm = radar_data.copy()
radar_data_norm[metric_cols] = radar_data_norm[metric_cols].div(radar_data_norm[metric_cols].max())

fig6 = go.Figure()
for _, row in radar_data_norm.iterrows():
    fig6.add_trace(go.Scatterpolar(
        r=row[metric_cols].values.tolist(),
        theta=metric_cols,
        fill='toself',
        name=row["country"]
    ))
fig6.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    title="Performance Radar by Country (Normalized)",
    showlegend=True
)
st.plotly_chart(fig6, use_container_width=True)

# --- INSIGHTS SUMMARY ---
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.subheader("🧠 Key Insights & Takeaways")

top_fund = fund_data.iloc[0]["country"]
top_val = corr.iloc[corr["valuation_busd"].idxmax()]["country"]
top_eff = eff.iloc[eff["efficiency"].idxmax()]["country"]

st.markdown(f"""
- 💸 **{top_fund}** leads in overall startup funding, signaling dominant investor confidence.
- 💎 **{top_val}** maintains the highest average valuation, reflecting a strong market reputation.
- ⚖️ **{top_eff}** shows the best *revenue-to-valuation* efficiency — most financially productive ecosystem.
- 🌍 Emerging countries with smaller ecosystems often yield **higher success scores** despite lower total funding.
- 👥 Employee size correlates loosely with valuation — larger teams don’t always mean higher efficiency.
""")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
