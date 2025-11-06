import pandas as pd

def calculate_kpis(df):
    kpis = {
        "Total Startups": len(df),
        "Total Funding ($M)": df["funding_musd"].sum(),
        "Avg Funding ($M)": df["funding_musd"].mean(),
        "Avg Valuation ($B)": df["valuation_busd"].mean(),
        "Avg Revenue ($M)": df["revenue_musd"].mean(),
        "Avg Employees": df["employees"].mean(),
        "IPO %": 100 * df["ipo"].mean(),
        "Acquired %": 100 * df["acquired"].mean(),
        "Avg Success Score": df["success_score"].mean(),
        "Avg Customers (M)": df["customers_mil"].mean(),
        "Top Country": df.groupby("country")["funding_musd"].sum().idxmax(),
        "Top Industry": df.groupby("industry")["funding_musd"].sum().idxmax(),
        "Median Funding ($M)": df["funding_musd"].median(),
        "Valuation / Funding Ratio": (df["valuation_busd"].sum() / df["funding_musd"].sum()) if df["funding_musd"].sum() > 0 else 0,
        "Top Tech Stack": df["tech_stack"].mode()[0] if "tech_stack" in df.columns and not df["tech_stack"].dropna().empty else "N/A",
        "Highest Success Startup": df.loc[df["success_score"].idxmax(), "name"],
        "Avg Funding per Employee": (df["funding_musd"].sum() / df["employees"].sum()) if df["employees"].sum() > 0 else 0,
        "Total Followers (M)": df["followers"].sum() / 1_000_000,
        "Avg Valuation / Employee": (df["valuation_busd"].sum() * 1000 / df["employees"].sum()) if df["employees"].sum() > 0 else 0,
    }
    return kpis
