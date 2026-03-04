import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_PATH = BASE_DIR / "data" / "aqi" / "current" / "aqi_current_timeseries.csv"


def predict_aqi_alert(city_name: str):
    df = pd.read_csv(DATA_PATH)

    df["city_clean"] = df["city"].str.strip().str.lower()
    city_name_clean = city_name.strip().lower()

    city_df = df[df["city_clean"] == city_name_clean]

    if city_df.empty:
        return {"error": "City not found"}

    city_df["timestamp"] = pd.to_datetime(city_df["timestamp"])

    # cutoff_time = datetime.now() - timedelta(hours=24)

    # recent_df = city_df[city_df["timestamp"] >= cutoff_time].copy()

    recent_df = city_df.copy()

    latest_row = recent_df.iloc[-1]

    latest_aqi = int(latest_row["aqi"])

    first_aqi = int(recent_df.iloc[0]["aqi"])

    trend = latest_aqi - first_aqi

    predicted_aqi = int(latest_aqi + trend)

    if predicted_aqi <= 50:
        risk = "Good"
    elif predicted_aqi <= 100:
        risk = "Satisfactory"
    elif predicted_aqi <= 200:
        risk = "Moderate"
    elif predicted_aqi <= 300:
        risk = "Poor"
    elif predicted_aqi <= 400:
        risk = "Very Poor"
    else:
        risk = "Severe"

    if predicted_aqi > 200:
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
