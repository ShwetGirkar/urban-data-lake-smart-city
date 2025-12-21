import pandas as pd
from utils import ensure_dir

WEATHER_FILE = "data/weather/current/weather_current_timeseries.csv"
AQI_FILE = "data/aqi/current/aqi_current_timeseries.csv"
TRAFFIC_FILE = "data/traffic/current/traffic_current_timeseries.csv"

OUTPUT_DIR = "data/processed"
OUTPUT_FILE = "city_current_snapshot.csv"


def latest_per_city(df):
    return df.sort_values("timestamp").groupby("city").tail(1)


def main():
    ensure_dir(OUTPUT_DIR)

    weather_df = pd.read_csv(WEATHER_FILE)
    aqi_df = pd.read_csv(AQI_FILE)
    traffic_df = pd.read_csv(TRAFFIC_FILE)

    weather_latest = latest_per_city(weather_df)
    aqi_latest = latest_per_city(aqi_df)
    traffic_latest = latest_per_city(traffic_df)

    merged = weather_latest.merge(
        aqi_latest,
        on=["city", "lat", "lon"],
        how="inner",
        suffixes=("_weather", "_aqi"),
    )

    merged = merged.merge(traffic_latest, on=["city", "lat", "lon"], how="inner")

    merged.to_csv(f"{OUTPUT_DIR}/{OUTPUT_FILE}", index=False)

    print("Merged dataset created:", f"{OUTPUT_DIR}/{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
