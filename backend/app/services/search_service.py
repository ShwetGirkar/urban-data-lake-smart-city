import pandas as pd
import requests
from pathlib import Path
from app.services.analytics_service import enrich_city_data
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2].parent
SNAPSHOT_PATH = BASE_DIR / "data" / "processed" / "city_current_snapshot.csv"


def search_location(query: str):
    df = pd.read_csv(SNAPSHOT_PATH)

    df["city_clean"] = df["city"].str.strip().str.lower()
    query_clean = query.strip().lower()

    # 1️⃣ Check if exists in dataset
    if query_clean in df["city_clean"].values:
        city_df = df[df["city_clean"] == query_clean]
        enriched = enrich_city_data(city_df)
        return {"source": "dataset", "data": enriched.to_dict(orient="records")[0]}

    # 2️⃣ If not found → live fetch
    return live_fetch(query)


OPENWEATHER_API_KEY = os.getenv("OWM_API_KEY")
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")


def live_fetch(query: str):
    # Geocoding
    formatted_query = query.replace(" ", ",")

    if ",IN" not in formatted_query.upper():
        formatted_query = formatted_query + ",IN"
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={formatted_query}&limit=1&appid={OPENWEATHER_API_KEY}"
    geo_response = requests.get(geo_url)
    geo_res = geo_response.json()

    # Debug protection
    if geo_response.status_code != 200:
        return {"error": "Geocoding API failed", "details": geo_res}

    if not isinstance(geo_res, list) or len(geo_res) == 0:
        return {"error": "Location not found"}

    lat = geo_res[0].get("lat")
    lon = geo_res[0].get("lon")

    if lat is None or lon is None:
        return {"error": "Invalid geocoding response"}

    # Weather
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    weather = requests.get(weather_url).json()

    # AQI
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    aqi = requests.get(aqi_url).json()

    # Traffic (TomTom)
    traffic_url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={TOMTOM_API_KEY}"
    traffic_response = requests.get(traffic_url)
    traffic = traffic_response.json()

    if "flowSegmentData" not in traffic:
        return {
            "error": "Traffic data not available for this location",
            "details": traffic,
        }

    current_speed = traffic["flowSegmentData"].get("currentSpeed")
    free_speed = traffic["flowSegmentData"].get("freeFlowSpeed")

    if not current_speed or not free_speed:
        return {"error": "Incomplete traffic data"}

    congestion_ratio = current_speed / free_speed

    aqi_value = aqi["list"][0]["main"]["aqi"]

    stress_score = (aqi_value / 5) * 0.6 + (1 - congestion_ratio) * 0.4

    return {
        "source": "live",
        "data": {
            "location": query,
            "lat": lat,
            "lon": lon,
            "temperature": weather["main"]["temp"],
            "aqi": aqi_value,
            "current_speed": current_speed,
            "free_flow_speed": free_speed,
            "congestion_ratio": congestion_ratio,
            "stress_score": stress_score,
        },
    }
