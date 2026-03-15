import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR.parent / "data" / "aqi" / "current" / "aqi_current_timeseries.csv"

PM25_BREAKPOINTS = [
    (0.0, 12.0, 0, 50),
    (12.1, 35.4, 51, 100),
    (35.5, 55.4, 101, 150),
    (55.5, 150.4, 151, 200),
    (150.5, 250.4, 201, 300),
    (250.5, 350.4, 301, 400),
    (350.5, 500.4, 401, 500),
]


def calculate_aqi_pm25(pm25):
    for bp_lo, bp_hi, aqi_lo, aqi_hi in PM25_BREAKPOINTS:
        if bp_lo <= pm25 <= bp_hi:
            return int(((aqi_hi - aqi_lo) / (bp_hi - bp_lo)) * (pm25 - bp_lo) + aqi_lo)
    return None


def get_air_quality_by_city(city_name: str):
    df = pd.read_csv(DATA_PATH)
    # Calculate US AQI from PM2.5
    df["aqi"] = df["pm25"].apply(calculate_aqi_pm25)
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
        risk = "Moderate"
    elif aqi_value <= 150:
        risk = "Unhealthy for Sensitive"
    elif aqi_value <= 200:
        risk = "Unhealthy"
    elif aqi_value <= 300:
        risk = "Very Unhealthy"
    else:
        risk = "Hazardous"
    # Convert trend values to proper Python types
    trend = city_df[["timestamp", "aqi", "pm25"]].copy()
    trend["aqi"] = trend["aqi"].astype(float)
    trend["pm25"] = trend["pm25"].astype(float)

    return {
        "city": city_name,
        "latest_aqi": aqi_value,
        "risk_level": risk,
        "aqi_trend": trend.to_dict(orient="records"),
    }
