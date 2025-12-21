import os
import requests
from dotenv import load_dotenv
from utils import ensure_dir, save_json, append_csv, utc_now
import pandas as pd

load_dotenv()

API_KEY = os.getenv("OWM_API_KEY")
CITIES = os.getenv("CITY").split(",")

OUTPUT_DIR = "data/weather/current"

print(os.getenv("OWM_API_KEY"))


def fetch_current_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city.strip(), "appid": API_KEY, "units": "metric"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def transform_current_weather(raw, city):
    return {
        "timestamp": utc_now(),
        "city": city,
        "lat": raw["coord"]["lat"],
        "lon": raw["coord"]["lon"],
        "temperature_c": raw["main"]["temp"],
        "feels_like_c": raw["main"]["feels_like"],
        "humidity_pct": raw["main"]["humidity"],
        "pressure_hpa": raw["main"]["pressure"],
        "wind_speed_mps": raw["wind"]["speed"],
        "weather_main": raw["weather"][0]["main"],
        "weather_description": raw["weather"][0]["description"],
    }


def main():
    ensure_dir(OUTPUT_DIR)

    for city in CITIES:
        try:
            raw = fetch_current_weather(city)
            save_json(OUTPUT_DIR, "weather_current_raw.json", raw)

            row = transform_current_weather(raw, city)
            append_csv(OUTPUT_DIR, "weather_current_timeseries.csv", row)

            print(f"Weather collected for {city}")

        except Exception as e:
            print(f"Error fetching weather for {city}: {e}")


if __name__ == "__main__":
    main()
