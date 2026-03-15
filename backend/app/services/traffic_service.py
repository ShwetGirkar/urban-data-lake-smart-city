import pandas as pd
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parents[2].parent
DATA_PATH = BASE_DIR / "data" / "traffic" / "current" / "traffic_current_timeseries.csv"


def get_traffic_by_city(city_name: str):

    df = pd.read_csv(DATA_PATH)

    df["city_clean"] = df["city"].str.strip().str.lower()
    city_name_clean = city_name.strip().lower()

    city_df = df[df["city_clean"] == city_name_clean]

    if city_df.empty:
        return None

    # city_df["timestamp"] = pd.to_datetime(city_df["timestamp"])

    # latest_time = city_df["timestamp"].max()
    # cutoff_time = latest_time - timedelta(hours=24)

    # city_df = city_df[city_df["timestamp"] >= cutoff_time]
    # city_df = city_df.sort_values("timestamp")
    # city_df = city_df.tail(24)

    # Compute congestion ratio
    city_df["congestion_ratio"] = 1 - (
        city_df["current_speed_kmh"] / city_df["free_flow_speed_kmh"].replace(0, pd.NA)
    )

    city_df["congestion_ratio"] = city_df["congestion_ratio"].clip(lower=0, upper=1)

    latest_row = city_df.iloc[-1]

    latest_speed = float(latest_row["current_speed_kmh"])

    latest_congestion = float(
        1 - (latest_row["current_speed_kmh"] / latest_row["free_flow_speed_kmh"])
    )

    trend = city_df[
        ["timestamp", "current_speed_kmh", "free_flow_speed_kmh", "congestion_ratio"]
    ].copy()

    trend["current_speed_kmh"] = trend["current_speed_kmh"].astype(float)
    trend["free_flow_speed_kmh"] = trend["free_flow_speed_kmh"].astype(float)
    trend["congestion_ratio"] = trend["congestion_ratio"].astype(float)

    # Peak congestion
    peak = city_df.sort_values("congestion_ratio", ascending=False).head(5)
    peak_data = peak[["timestamp", "congestion_ratio"]].to_dict(orient="records")

    return {
        "city": city_name,
        "latest_speed": latest_speed,
        "latest_congestion_ratio": latest_congestion,
        "traffic_trend": trend.to_dict(orient="records"),
        "peak_hours": peak_data,
    }
