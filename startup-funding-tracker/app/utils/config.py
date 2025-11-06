import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = os.getenv("PROJECT_NAME", "Startup Intelligence Dashboard")
DB_PATH = os.getenv("DB_PATH", "db/funding.db")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "Global")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

COLOR_PRIMARY = "#0072B5"
COLOR_SECONDARY = "#F4B400"

# For display precision
CURRENCY = "USD"
