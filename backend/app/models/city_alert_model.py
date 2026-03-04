import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data" / "processed" / "city_current_snapshot.csv"


def generate_city_alerts():

    df = pd.read_csv(DATA_PATH)

    alerts = []

    for _, row in df.iterrows():
        city = row["city"]

        # AQI Alert
        if row["aqi"] > 200:
            alerts.append({"city": city, "alert": "Severe Air Pollution"})

        # Traffic Alert
        speed_ratio = row["current_speed_kmh"] / row["free_flow_speed_kmh"]

        if speed_ratio < 0.5:
            alerts.append({"city": city, "alert": "Severe Traffic Congestion"})

    return alerts
