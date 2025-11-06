import streamlit as st
import pandas as pd
import plotly.express as px
from utils.filters import load_data, sidebar_filters

# --- PAGE CONFIG ---
st.set_page_config(page_title="Industry Insights", page_icon="📊", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
.section-header {
    font-size: 26px;
    color: #1A5276;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 15px;
    border-left: 5px solid #2E86C1;
    padding-left: 12px;
}
.insight-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    padding: 15px 20px;
    margin-bottom: 15px;
}
.metric {
    font-size: 26px;
    color: #2E86C1;
    font-weight: 700;
}
.label {
    font-size: 14px;
    color: #616A6B;
}
.divider {
    border-top: 2px solid #E5E8E8;
    margin: 40px 0px;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("📊 Industry Insights")
st.caption("Analyze funding, valuation, workforce, and performance metrics across industries.")

# --- LOAD & FILTER DATA ---
df = sidebar_filters(load_data())

if df.empty:
    st.warning("⚠️ No data available for selected filters. Try adjusting the filters in the sidebar.")
    st.stop()

# --- KPI CARDS ---
st.markdown('<p class="section-header">💡 Key Industry Statistics</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="insight-card"><div class="metric">'
                f"{df['industry'].nunique()}</div><div class='label'>Active Industries</div></div>", unsafe_allow_html=True)
with col2:
    top_fund_ind = df.groupby("industry")["funding_musd"].sum().idxmax()
    st.markdown('<div class="insight-card"><div class="metric">'
                f"{top_fund_ind}</div><div class='label'>Top Funded Industry</div></div>", unsafe_allow_html=True)
with col3:
    top_val_ind = df.groupby("industry")["valuation_busd"].mean().idxmax()
    st.markdown('<div class="insight-card"><div class="metric">'
                f"{top_val_ind}</div><div class='label'>Highest Valuation Industry</div></div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- FUNDING DISTRIBUTION ---
st.markdown('<p class="section-header">💰 Funding Distribution by Industry</p>', unsafe_allow_html=True)
funding_data = df.groupby("industry")["funding_musd"].sum().sort_values(ascending=False).head(10).reset_index()
fig = px.bar(funding_data, x="funding_musd", y="industry", orientation="h",
             title="Top 10 Industries by Funding", color="funding_musd", color_continuous_scale="Blues")
st.plotly_chart(fig, use_container_width=True)

# --- AVERAGE VALUATION ---
st.markdown('<p class="section-header">💎 Average Valuation by Industry</p>', unsafe_allow_html=True)
valuation_data = df.groupby("industry")["valuation_busd"].mean().sort_values(ascending=False).head(10).reset_index()
fig2 = px.pie(valuation_data, names="industry", values="valuation_busd",
              title="Average Valuation ($B) Distribution by Industry", hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

# --- FUNDING vs SUCCESS ---
st.markdown('<p class="section-header">📈 Funding vs Success Score</p>', unsafe_allow_html=True)
corr_data = df.groupby("industry")[["funding_musd", "success_score"]].mean().reset_index()
fig3 = px.scatter(corr_data, x="funding_musd", y="success_score", size="success_score",
                  color="industry", hover_name="industry",
                  title="Correlation Between Funding and Success by Industry")
st.plotly_chart(fig3, use_container_width=True)

# --- EMPLOYEE SCALE ---
st.markdown('<p class="section-header">👥 Average Employees per Industry</p>', unsafe_allow_html=True)
emp_data = df.groupby("industry")["employees"].mean().sort_values(ascending=False).reset_index()
fig4 = px.bar(emp_data, x="industry", y="employees", title="Average Employees by Industry",
              color="employees", color_continuous_scale="Purples")
st.plotly_chart(fig4, use_container_width=True)

# --- REVENUE-VALUATION RATIO ---
st.markdown('<p class="section-header">⚖️ Revenue-to-Valuation Ratio</p>', unsafe_allow_html=True)
ratio_data = df.groupby("industry")[["revenue_musd", "valuation_busd"]].mean().reset_index()
ratio_data["efficiency_ratio"] = ratio_data["revenue_musd"] / ratio_data["valuation_busd"]
ratio_data = ratio_data.sort_values("efficiency_ratio", ascending=False)
fig5 = px.bar(ratio_data, x="efficiency_ratio", y="industry", orientation="h",
              title="Revenue Efficiency by Industry", color="efficiency_ratio", color_continuous_scale="Tealgrn")
st.plotly_chart(fig5, use_container_width=True)

# --- HEATMAP (BONUS) ---
st.markdown('<p class="section-header">🔥 Multi-Metric Comparison (Heatmap)</p>', unsafe_allow_html=True)
heat_data = df.groupby("industry")[["funding_musd", "valuation_busd", "success_score", "employees", "revenue_musd"]].mean().reset_index()
fig6 = px.imshow(
    heat_data.set_index("industry").T,
    aspect="auto",
    color_continuous_scale="Blues",
    title="Industry Performance Comparison Matrix"
)
st.plotly_chart(fig6, use_container_width=True)

# --- SUMMARY INSIGHTS ---
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.subheader("🧠 Key Takeaways")

top_fund = funding_data.iloc[0]["industry"]
top_val = valuation_data.iloc[0]["industry"]
top_eff = ratio_data.iloc[0]["industry"]

st.markdown(f"""
- 💸 **{top_fund}** receives the most funding overall — a hotspot for investors.  
- 💎 **{top_val}** leads in valuation, showing higher market potential.  
- ⚖️ **{top_eff}** demonstrates the best financial efficiency (revenue-to-valuation).  
- 📈 Industries with mid-level funding often show **better success efficiency**.  
- 👥 Workforce-heavy sectors tend to align with higher valuations and funding.  
""")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
