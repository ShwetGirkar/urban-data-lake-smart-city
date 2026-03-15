import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_PATH = BASE_DIR / "data" / "aqi" / "current" / "aqi_current_timeseries.csv"

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


def predict_aqi_alert(city_name: str):
    df = pd.read_csv(DATA_PATH)

    df["aqi"] = df["pm25"].apply(calculate_aqi_pm25)

    df["city_clean"] = df["city"].str.strip().str.lower()
    city_name_clean = city_name.strip().lower()

    city_df = df[df["city_clean"] == city_name_clean]
    city_df = city_df.copy()

    if city_df.empty:
        return {"error": "City not found"}

    city_df["timestamp"] = pd.to_datetime(city_df["timestamp"])
    city_df = city_df.sort_values("timestamp")

    latest_time = city_df["timestamp"].max()
    cutoff_time = latest_time - timedelta(hours=24)

    recent_df = city_df[city_df["timestamp"] >= cutoff_time].copy()
    recent_df = recent_df.sort_values("timestamp")

    if recent_df.empty:
        return {"error": "No recent AQI data"}
    # recent_df = city_df.copy().tail(5)

    latest_aqi = int(recent_df["aqi"].iloc[-1])
    first_aqi = int(recent_df["aqi"].iloc[0])

    trend = max(-50, min(50, latest_aqi - first_aqi))

    predicted_aqi = int(latest_aqi + trend)

    # clamp to valid AQI range
    predicted_aqi = max(0, min(predicted_aqi, 500))

    if predicted_aqi <= 50:
        risk = "Good"
    elif predicted_aqi <= 100:
        risk = "Moderate"
    elif predicted_aqi <= 150:
        risk = "Unhealthy for Sensitive"
    elif predicted_aqi <= 200:
        risk = "Unhealthy"
    elif predicted_aqi <= 300:
        risk = "Very Unhealthy"
    else:
        risk = "Hazardous"

    if predicted_aqi >= 200:
        alert = "High Pollution Risk"
    else:
        alert = "Normal"

    return {
        "city": city_name,
        "latest_aqi": latest_aqi,
        "predicted_aqi": predicted_aqi,
        "trend": trend,
        "risk_level": risk,
        "alert": alert,
    }
