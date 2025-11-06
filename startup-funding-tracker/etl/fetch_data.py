from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

DATASET = RAW / "global_startup_success_dataset.csv"

if not DATASET.exists():
    raise FileNotFoundError("⚠️ Please place your dataset in data/raw/global_startup_success_dataset.csv")

df = pd.read_csv(DATASET)
print(f"✅ Loaded {len(df)} records from {DATASET}")
print(f"Columns detected: {list(df.columns)}")
