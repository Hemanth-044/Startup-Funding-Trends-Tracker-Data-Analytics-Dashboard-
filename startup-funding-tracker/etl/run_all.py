import os
from pathlib import Path

# Detect project root dynamically
ROOT = Path(__file__).resolve().parents[1]
ETL_DIR = ROOT / "etl"

print("🚀 Running full ETL pipeline...")

# Run scripts with absolute paths
os.system(f'python "{ETL_DIR / "fetch_data.py"}"')
os.system(f'python "{ETL_DIR / "clean_transform.py"}"')
os.system(f'python "{ETL_DIR / "load_to_sqlite.py"}"')

print("✅ ETL pipeline complete.")
