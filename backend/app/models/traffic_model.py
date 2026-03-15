import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_PATH = BASE_DIR / "data" / "traffic" / "current" / "traffic_current_timeseries.csv"


def predict_peak_hours(city_name: str):
    df = pd.read_csv(DATA_PATH)

    df["city_clean"] = df["city"].str.strip().str.lower()
    city_name_clean = city_name.strip().lower()

    city_df = df[df["city_clean"] == city_name_clean]

    if city_df.empty:
        return {"error": "City not found in traffic dataset"}

    city_df["timestamp"] = pd.to_datetime(city_df["timestamp"])

    # change when we have 3 days worth of data

    # cutoff_time = datetime.now() - timedelta(hours=48)

    # recent_df = city_df[city_df["timestamp"] >= cutoff_time].copy()
    recent_df = city_df.copy()

    recent_df["congestion"] = (
        recent_df["current_speed_kmh"] / recent_df["free_flow_speed_kmh"]
    )
    recent_df["hour"] = recent_df["timestamp"].dt.hour

    hourly_congestion = recent_df.groupby("hour")["congestion"].mean().reset_index()

    top_hours = hourly_congestion.sort_values("congestion", ascending=False).head(5)

    return {"city": city_name, "peak_hours": top_hours.to_dict(orient="records")}
