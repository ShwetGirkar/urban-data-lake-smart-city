import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

TRAFFIC_PATH = (
    BASE_DIR / "data" / "traffic" / "current" / "traffic_current_timeseries.csv"
)
AQI_PATH = BASE_DIR / "data" / "aqi" / "current" / "aqi_current_timeseries.csv"
WEATHER_PATH = (
    BASE_DIR / "data" / "weather" / "current" / "weather_current_timeseries.csv"
)


def calculate_urban_stress(city_name: str):
    traffic_df = pd.read_csv(TRAFFIC_PATH)
    aqi_df = pd.read_csv(AQI_PATH)
    weather_df = pd.read_csv(WEATHER_PATH)

    city_name_clean = city_name.strip().lower()

    traffic_df["city_clean"] = traffic_df["city"].str.strip().str.lower()
    aqi_df["city_clean"] = aqi_df["city"].str.strip().str.lower()
    weather_df["city_clean"] = weather_df["city"].str.strip().str.lower()

    traffic_city = traffic_df[traffic_df["city_clean"] == city_name_clean]
    aqi_city = aqi_df[aqi_df["city_clean"] == city_name_clean]
    weather_city = weather_df[weather_df["city_clean"] == city_name_clean]

    traffic_row = traffic_city.iloc[-1]
    aqi_row = aqi_city.iloc[-1]
    weather_row = weather_city.iloc[-1]

    # traffic score
    traffic_congestion = 1 - (
        traffic_row["current_speed_kmh"] / traffic_row["free_flow_speed_kmh"]
    )

    traffic_score = float(traffic_congestion)

    # pollution score
    pollution_score = float(aqi_row["aqi"]) / 500

    # weather score
    temp = weather_row["temperature_c"]
    weather_score = abs(temp - 22) / 20
    weather_score = min(weather_score, 1)

    # calculate urban stress
    stress_index = (
        (traffic_score * 0.4) + (pollution_score * 0.4) + (weather_score * 0.2)
    )
    stress_index = float(stress_index)

    if stress_index <= 0.3:
        level = "Low"
    elif stress_index <= 0.6:
        level = "Moderate"
    elif stress_index <= 0.8:
        level = "High"
    else:
        level = "Critical"

    return {
        "city": city_name,
        "urban_stress_index": stress_index,
        "stress_level": level,
        "drivers": {
            "traffic": traffic_score,
            "pollution": pollution_score,
            "weather": weather_score,
        },
    }


def rank_cities_by_stress():
    traffic_df = pd.read_csv(TRAFFIC_PATH)
    aqi_df = pd.read_csv(AQI_PATH)
    weather_df = pd.read_csv(WEATHER_PATH)

    cities = traffic_df["city"].unique()

    ranking = []

    for city in cities:
        result = calculate_urban_stress(city)
        ranking.append(
            {
                "city": city,
                "stress_index": result["urban_stress_index"],
                "level": result["stress_level"],
            }
        )

    ranking_df = pd.DataFrame(ranking)

    ranking_df = ranking_df.sort_values("stress_index", ascending=False)

    ranking_df = ranking_df.head(5)

    return ranking_df.to_dict(orient="records")
