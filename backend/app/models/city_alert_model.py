import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data" / "processed" / "city_current_snapshot.csv"

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


def generate_city_alerts():

    df = pd.read_csv(DATA_PATH)

    df["aqi"] = df["pm25"].apply(calculate_aqi_pm25)

    alerts = []

    for _, row in df.iterrows():
        city = row["city"]

        # AQI Alert
        if row["aqi"] >= 300:
            alerts.append({"city": city, "alert": "Hazardous Air Quality"})
        elif row["aqi"] >= 200:
            alerts.append({"city": city, "alert": "Very Unhealthy Air"})
        elif row["aqi"] >= 150:
            alerts.append({"city": city, "alert": "Unhealthy Air Quality"})
        # Traffic Alert
        free_speed = row["free_flow_speed_kmh"]

        if free_speed > 0:
            speed_ratio = row["current_speed_kmh"] / free_speed
        else:
            speed_ratio = 1

        if speed_ratio < 0.4:
            alerts.append({"city": city, "alert": "Severe Traffic Congestion"})
        elif speed_ratio < 0.6:
            alerts.append({"city": city, "alert": "Heavy Traffic"})

    return alerts
