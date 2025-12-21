import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from utils import ensure_dir, save_json, append_csv, utc_now

load_dotenv()

API_KEY = os.getenv("OWM_API_KEY")

WEATHER_FILE = "data/weather/current/weather_current_timeseries.csv"
OUTPUT_DIR = "data/aqi/current"


def get_latest_city_coordinates():
    df = pd.read_csv(WEATHER_FILE)

    latest = df.sort_values("timestamp").groupby("city").tail(1)

    city_coords = {}
    for _, row in latest.iterrows():
        city_coords[row["city"]] = {"lat": row["lat"], "lon": row["lon"]}

    return city_coords


def fetch_aqi(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def transform_aqi(raw, city, lat, lon):
    data = raw["list"][0]
    comp = data["components"]

    return {
        "timestamp": utc_now(),
        "city": city,
        "lat": lat,
        "lon": lon,
        "aqi": data["main"]["aqi"],
        "pm25": comp["pm2_5"],
        "pm10": comp["pm10"],
        "no2": comp["no2"],
        "so2": comp["so2"],
        "co": comp["co"],
        "o3": comp["o3"],
    }


def main():
    ensure_dir(OUTPUT_DIR)

    city_coords = get_latest_city_coordinates()

    for city, coords in city_coords.items():
        try:
            raw = fetch_aqi(coords["lat"], coords["lon"])
            save_json(OUTPUT_DIR, "aqi_current_raw.json", raw)

            row = transform_aqi(raw, city, coords["lat"], coords["lon"])

            append_csv(OUTPUT_DIR, "aqi_current_timeseries.csv", row)

            print(f"AQI collected for {city}")

        except Exception as e:
            print(f"Error fetching AQI for {city}: {e}")


if __name__ == "__main__":
    main()
