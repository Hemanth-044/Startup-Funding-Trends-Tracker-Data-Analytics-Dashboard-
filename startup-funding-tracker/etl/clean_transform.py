import pandas as pd
from pathlib import Path
import uuid

RAW = Path("data/raw")
INTERIM = Path("data/interim")
INTERIM.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW / "global_startup_success_dataset.csv")


rename_map = {
    "Startup Name": "name",
    "Founded Year": "founded_year",
    "Country": "country",
    "Industry": "industry",
    "Funding Stage": "funding_stage",
    "Total Funding ($M)": "funding_musd",
    "Number of Employees": "employees",
    "Annual Revenue ($M)": "revenue_musd",
    "Valuation ($B)": "valuation_busd",
    "Success Score": "success_score",
    "Acquired?": "acquired",
    "IPO?": "ipo",
    "Customer Base (Millions)": "customers_mil",
    "Tech Stack": "tech_stack",
    "Social Media Followers": "followers"
}
df.rename(columns=rename_map, inplace=True)

df["acquired"] = df["acquired"].str.lower().map({"yes": 1, "no": 0})
df["ipo"] = df["ipo"].str.lower().map({"yes": 1, "no": 0})

df["followers"] = (
    df["followers"].replace({"M": "e6", "K": "e3"}, regex=True)
    .apply(lambda x: pd.eval(x) if isinstance(x, str) else x)
)

df["startup_id"] = [
    str(uuid.uuid5(uuid.NAMESPACE_DNS, str(name) + str(country)))
    for name, country in zip(df["name"], df["country"])
]

df.to_csv(INTERIM / "startups_clean.csv", index=False)
print("✅ Cleaned data saved to data/interim/startups_clean.csv")
