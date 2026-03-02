import pandas as pd
from pathlib import Path

# Get project root (go up from backend/app/services)
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR.parent / "data" / "processed" / "city_current_snapshot.csv"


def load_city_snapshot():
    df = pd.read_csv(DATA_PATH)
    return df
