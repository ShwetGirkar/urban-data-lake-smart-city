import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from utils import ensure_dir, save_json, append_csv, utc_now

load_dotenv()

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

WEATHER_FILE = "data/weather/current/weather_current_timeseries.csv"
OUTPUT_DIR = "data/traffic/current"


def get_latest_city_coordinates():
    df = pd.read_csv(WEATHER_FILE)

    latest = df.sort_values("timestamp").groupby("city").tail(1)

    city_coords = {}
    for _, row in latest.iterrows():
        city_coords[row["city"]] = {"lat": row["lat"], "lon": row["lon"]}

    return city_coords


def fetch_traffic(lat, lon):
    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    params = {"key": TOMTOM_API_KEY, "point": f"{lat},{lon}"}

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def transform_traffic(raw, city, lat, lon):
    flow = raw["flowSegmentData"]

    return {
        "timestamp": utc_now(),
        "city": city,
        "lat": lat,
        "lon": lon,
        "current_speed_kmh": flow["currentSpeed"],
        "free_flow_speed_kmh": flow["freeFlowSpeed"],
        "confidence": flow["confidence"],
        "road_closure": flow.get("roadClosure", False),
    }


def main():
    ensure_dir(OUTPUT_DIR)

    city_coords = get_latest_city_coordinates()

    for city, coords in city_coords.items():
        try:
            raw = fetch_traffic(coords["lat"], coords["lon"])
            save_json(OUTPUT_DIR, "traffic_current_raw.json", raw)

            row = transform_traffic(raw, city, coords["lat"], coords["lon"])

            append_csv(OUTPUT_DIR, "traffic_current_timeseries.csv", row)

            print(f"Traffic collected for {city}")

        except Exception as e:
            print(f"Error fetching traffic for {city}: {e}")


if __name__ == "__main__":
    main()
