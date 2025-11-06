import streamlit as st
import pandas as pd
from utils.filters import load_data, sidebar_filters
from utils.kpis import calculate_kpis
from utils.charts import pie_chart, bar_chart, donut_chart

# --- CONFIG ---
st.set_page_config(
    page_title="Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
body {
    background-color: #f9fafc;
}

/* --- Titles --- */
.main-title {
    font-size: 55px;
    font-weight: 800;
    color: #154360;
    text-align: center;
    padding-top: 10px;
    letter-spacing: 0.5px;
}
.sub-title {
    text-align: center;
    font-size: 20px;
    color: #626567;
    margin-top: -15px;
    margin-bottom: 40px;
}

/* --- Section Headers --- */
.section-header {
    font-size: 26px;
    color: #1A5276;
    font-weight: 700;
    margin-top: 40px;
    margin-bottom: 10px;
    border-left: 5px solid #2E86C1;
    padding-left: 12px;
}

/* --- KPI Card Styling --- */
.kpi-card {
    background-color: white;
    border-radius: 18px;
    padding: 20px 30px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    text-align: center;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    border-top: 4px solid #2E86C1;
}
.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.12);
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #2E86C1;
}
.kpi-label {
    font-size: 15px;
    color: #616A6B;
    font-weight: 600;
    margin-top: 6px;
}
.highlight-card {
    background: linear-gradient(135deg, #1ABC9C, #16A085);
    color: white;
    border: none;
}
.highlight-card .kpi-value, .highlight-card .kpi-label {
    color: white !important;
}

/* --- Divider --- */
.divider {
    border-top: 2px solid #E5E8E8;
    margin: 40px 0px;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="main-title">🌍 Global Startup Intelligence Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Insightful analytics on 5,000+ startups across 10 countries — funding, valuation, success, and industry trends.</p>', unsafe_allow_html=True)

# --- INTRO SECTION ---
with st.expander("📘 About this Project", expanded=True):
    st.markdown("""
    This dashboard provides a **data-driven exploration of global startup ecosystems**, revealing patterns in:
    - 💵 Funding distribution across sectors and countries  
    - 💎 Valuation and revenue trends  
    - 🚀 Success rates and acquisition/IPO statistics  
    - 🧠 Emerging industries and tech stacks  

    **Purpose:** Empower entrepreneurs, analysts, and investors with real-time, actionable insights.
    """)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- LOAD & FILTER DATA ---
df = sidebar_filters(load_data())

# --- HANDLE EMPTY FILTER RESULT ---
if df is None or df.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your filters to view insights.")
    st.stop()

# --- KPI SECTION ---
st.markdown('<p class="section-header">📈 Key Performance Indicators</p>', unsafe_allow_html=True)
kpis = calculate_kpis(df)

cols = st.columns(4)
for i, (key, val) in enumerate(kpis.items()):
    card_class = "kpi-card highlight-card" if "Highest Success Startup" in key else "kpi-card"
    val_display = f"{val:,.2f}" if isinstance(val, (int, float)) else val

    with cols[i % 4]:
        st.markdown(
            f"""
            <div class="{card_class}">
                <div class="kpi-value">{val_display}</div>
                <div class="kpi-label">{key}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- INSIGHTS SECTION ---
st.markdown('<p class="section-header">🏭 Industry & Market Insights</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if not df.empty:
        industry_data = df.groupby("industry")["funding_musd"].sum().sort_values(ascending=False).head(10).reset_index()
        if not industry_data.empty:
            st.plotly_chart(bar_chart(industry_data, "industry", "funding_musd", "Top 10 Industries by Total Funding ($M)"), use_container_width=True)
        else:
            st.info("No industry data available for current selection.")
    else:
        st.info("No data available for current filters.")

with col2:
    if not df.empty:
        country_data = df.groupby("country")["funding_musd"].sum().reset_index()
        if not country_data.empty:
            st.plotly_chart(donut_chart(country_data, "country", "funding_musd", "Funding Distribution by Country"), use_container_width=True)
        else:
            st.info("No country data available for current selection.")
    else:
        st.info("No data available for current filters.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- VALUATION & SUCCESS SECTION ---
st.markdown('<p class="section-header">💎 Valuation and Success Patterns</p>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    if not df.empty:
        top_valuation = df.groupby("industry")["valuation_busd"].mean().sort_values(ascending=False).head(10).reset_index()
        if not top_valuation.empty:
            st.plotly_chart(pie_chart(top_valuation, "industry", "valuation_busd", "Average Valuation by Industry ($B)"), use_container_width=True)
        else:
            st.info("No valuation data available.")
    else:
        st.info("No data available for current filters.")

with col4:
    if not df.empty:
        success_by_country = df.groupby("country")["success_score"].mean().sort_values(ascending=False).head(10).reset_index()
        if not success_by_country.empty:
            st.plotly_chart(bar_chart(success_by_country, "country", "success_score", "Average Success Score by Country"), use_container_width=True)
        else:
            st.info("No success data available.")
    else:
        st.info("No data available for current filters.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- FOOTER SECTION ---
st.markdown("""
### 🧭 Explore More:
Use the **sidebar filters** to narrow your focus by country, industry, or founding year.  
Dive into other pages for detailed insights:
- 📊 Industry Analytics  
- 🌍 Country Comparisons  
- 📅 Trends Over Time  
- 🚀 Success Drivers  
- 💼 Acquisitions & IPOs  
- 🔍 Custom Data Explorer  

---
**👨‍💻 Developed by:** J Hemanth Kumar  
**📅 Dataset:** Global Startup Success (5,000 startups, 15 attributes) https://www.kaggle.com/datasets/hamnakaleemds/global-startup-success-dataset/data  
**⚙️ Tech Stack:** Python • Streamlit • Plotly • Pandas • SQLite  
""")
