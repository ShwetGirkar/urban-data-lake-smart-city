from fastapi import APIRouter
from app.services.data_loader import load_city_snapshot
from app.services.analytics_service import compute_summary

router = APIRouter()


@router.get("/api/summary")
def get_summary():
    df = load_city_snapshot()
    return compute_summary(df)


@router.get("/api/status")
def get_status():
    df = load_city_snapshot()
    df["timestamp_weather"] = df["timestamp_weather"]

    last_updated = df["timestamp_weather"].max()
    total_cities = len(df)

    return {
        "system_status": "running",
        "total_cities": total_cities,
        "last_updated": last_updated,
    }
