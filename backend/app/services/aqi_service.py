import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR.parent / "data" / "aqi" / "current" / "aqi_current_timeseries.csv"


def get_air_quality_by_city(city_name: str):
    df = pd.read_csv(DATA_PATH)

    # Clean city names
    df["city_clean"] = df["city"].str.strip().str.lower()
    city_name_clean = city_name.strip().lower()

    city_df = df[df["city_clean"] == city_name_clean]

    if city_df.empty:
        return None

    # Sort by timestamp
    city_df = city_df.sort_values("timestamp")

    latest_row = city_df.iloc[-1]

    # Risk classification
    aqi_value = int(latest_row["aqi"])  # ← convert to normal int

    if aqi_value <= 50:
        risk = "Good"
    elif aqi_value <= 100:
        risk = "Satisfactory"
    elif aqi_value <= 200:
        risk = "Moderate"
    elif aqi_value <= 300:
        risk = "Poor"
    elif aqi_value <= 400:
        risk = "Very Poor"
    else:
        risk = "Severe"

    # Convert trend values to proper Python types
    trend = city_df[["timestamp", "aqi", "pm25"]].copy()
    trend["aqi"] = trend["aqi"].astype(int)
    trend["pm25"] = trend["pm25"].astype(float)

    return {
        "city": city_name,
        "latest_aqi": aqi_value,
        "risk_level": risk,
        "aqi_trend": trend.to_dict(orient="records"),
    }
