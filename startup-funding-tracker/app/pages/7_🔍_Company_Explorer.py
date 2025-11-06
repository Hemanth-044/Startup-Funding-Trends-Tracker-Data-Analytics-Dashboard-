import streamlit as st
import pandas as pd
import plotly.express as px
from utils.filters import load_data, sidebar_filters

# --- PAGE CONFIG ---
st.set_page_config(page_title="Company Explorer", page_icon="🔍", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
.section-header {
    font-size: 26px;
    color: #1A5276;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 10px;
    border-left: 5px solid #2E86C1;
    padding-left: 12px;
}
.metric-card {
    background-color: white;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    padding: 18px 20px;
    text-align: center;
    margin-bottom: 15px;
}
.metric-value {
    font-size: 26px;
    color: #2E86C1;
    font-weight: 700;
}
.metric-label {
    font-size: 14px;
    color: #616A6B;
    font-weight: 600;
}
.insight-box {
    background: linear-gradient(135deg, #EBF5FB, #E8F8F5);
    border-radius: 12px;
    padding: 18px 22px;
    font-size: 15px;
    color: #154360;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
}
.divider {
    border-top: 2px solid #E5E8E8;
    margin: 25px 0px;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🔍 Company Explorer")
st.caption("Search or select a company to get detailed insights into its funding, valuation, and success profile.")

# --- LOAD DATA ---
df = sidebar_filters(load_data())
if df.empty:
    st.warning("⚠️ No data available for the selected filters.")
    st.stop()

# --- NORMALIZE COLUMNS ---
df.columns = df.columns.str.strip().str.lower().str.replace('[^a-z0-9]+', '_', regex=True)

# Uncomment this to debug:
# st.write("🧩 Columns detected:", list(df.columns))

# --- FORCE NAME COLUMN (From your DB schema) ---
if "name" not in df.columns:
    st.error("❌ Expected a 'name' column in the dataset (from your database schema). Please verify ETL consistency.")
    st.stop()

name_col = "name"

# --- FILTER VALID NAMES ---
df = df[df[name_col].notna() & (df[name_col].str.strip() != "")]
companies = sorted(df[name_col].unique().tolist())

# --- COMPANY DROPDOWN ---
selected_name = st.selectbox(
    "🔎 Search for a Company",
    options=companies,
    index=None,
    placeholder="Type or select a company (e.g., Zomato, Paytm, Swiggy)..."
)

if not selected_name:
    st.info("Please select a company from the dropdown to view detailed insights.")
    st.stop()

# --- FETCH COMPANY DATA ---
company_data = df[df[name_col] == selected_name]
if company_data.empty:
    st.warning("No matching company found in the dataset.")
    st.stop()

company_row = company_data.iloc[0]

# --- DISPLAY OVERVIEW ---
st.markdown(f"<p class='section-header'>🏢 Overview — {company_row[name_col]}</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='metric-card'><div class='metric-value'>{company_row.get('country','N/A')}</div><div class='metric-label'>Country</div></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-card'><div class='metric-value'>{company_row.get('industry','N/A')}</div><div class='metric-label'>Industry</div></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-card'><div class='metric-value'>{int(company_row.get('founded_year',0))}</div><div class='metric-label'>Founded Year</div></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-card'><div class='metric-value'>{company_row.get('funding_stage','N/A')}</div><div class='metric-label'>Funding Stage</div></div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- TABS ---
tabs = st.tabs(["📊 Financials", "🚀 Success Metrics", "🌍 Context & Comparison", "🧠 Insights Summary"])

# --- FINANCIALS TAB ---
with tabs[0]:
    st.markdown("<p class='section-header'>💰 Funding & Valuation</p>", unsafe_allow_html=True)

    funding = company_row.get("funding_musd", 0)
    valuation = company_row.get("valuation_busd", 0)
    revenue = company_row.get("revenue_musd", 0)

    colf1, colf2, colf3 = st.columns(3)
    colf1.metric("Total Funding ($M)", f"{funding:,.2f}")
    colf2.metric("Valuation ($B)", f"{valuation:,.2f}")
    colf3.metric("Annual Revenue ($M)", f"{revenue:,.2f}")

    if "funding_stage" in df.columns:
        stage_df = df.groupby("funding_stage")["funding_musd"].mean().reset_index()
        fig_stage = px.bar(
            stage_df,
            x="funding_stage", y="funding_musd",
            color="funding_stage",
            title="Average Funding by Stage",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_stage, use_container_width=True)

# --- SUCCESS TAB ---
with tabs[1]:
    st.markdown("<p class='section-header'>🚀 Success Indicators</p>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Success Score", f"{company_row.get('success_score',0):.2f}")
    col2.metric("Customers (M)", f"{company_row.get('customers_mil',0):.2f}")
    col3.metric("Employees", int(company_row.get('employees',0)))
    col4.metric("Social Followers", f"{company_row.get('followers',0):,.0f}")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    fig_success = px.bar(
        x=["Success Score", "Customers", "Revenue", "Valuation"],
        y=[
            company_row.get("success_score", 0),
            company_row.get("customers_mil", 0),
            company_row.get("revenue_musd", 0),
            company_row.get("valuation_busd", 0),
        ],
        color=["Success Score", "Customers", "Revenue", "Valuation"],
        title="Company Strength Overview",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    st.plotly_chart(fig_success, use_container_width=True)

# --- CONTEXT TAB ---
with tabs[2]:
    st.markdown("<p class='section-header'>🌍 Market & Industry Context</p>", unsafe_allow_html=True)

    same_industry = df[df["industry"] == company_row["industry"]]
    same_country = df[df["country"] == company_row["country"]]

    col1, col2 = st.columns(2)

    with col1:
        if not same_industry.empty:
            industry_avg = same_industry[["funding_musd", "valuation_busd", "success_score"]].mean().to_dict()
            st.markdown(f"### 🏭 {company_row['industry']} Industry Averages")
            st.write(pd.DataFrame([industry_avg], index=["Average"]))
        else:
            st.info("No industry data available for comparison.")

    with col2:
        if not same_country.empty:
            country_avg = same_country[["funding_musd", "valuation_busd", "success_score"]].mean().to_dict()
            st.markdown(f"### 🌎 {company_row['country']} Country Averages")
            st.write(pd.DataFrame([country_avg], index=["Average"]))
        else:
            st.info("No country data available for comparison.")

# --- INSIGHTS TAB ---
with tabs[3]:
    st.markdown("<p class='section-header'>🧠 AI-Style Insights</p>", unsafe_allow_html=True)

    insights = []
    if company_row.get("funding_musd", 0) > df["funding_musd"].mean():
        insights.append("💰 Above-average funding — strong investor confidence.")
    if company_row.get("success_score", 0) > df["success_score"].mean():
        insights.append("🚀 Exceptional success metrics — performing better than peers.")
    if company_row.get("valuation_busd", 0) > df["valuation_busd"].mean():
        insights.append("💎 High valuation suggests category leadership or market dominance.")
    if company_row.get("customers_mil", 0) > df["customers_mil"].mean():
        insights.append("👥 Strong customer base — indicates market traction.")
    if company_row.get("employees", 0) > df["employees"].mean():
        insights.append("👨‍💻 Scaled operations — larger workforce than average for its sector.")
    if not insights:
        insights.append("📊 This company maintains balanced performance across all major KPIs.")

    st.markdown(f"<div class='insight-box'>{'<br>'.join(insights)}</div>", unsafe_allow_html=True)
