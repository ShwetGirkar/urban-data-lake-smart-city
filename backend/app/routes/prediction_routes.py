from fastapi import APIRouter
from app.services.prediction_service import (
    get_traffic_prediction,
    get_aqi_prediction,
    get_city_stress,
    get_stress_ranking,
    get_city_alerts,
)


router = APIRouter()


@router.get("/api/predict/traffic/{city}")
def predict_traffic(city: str):
    result = get_traffic_prediction(city)
    return result


@router.get("/api/predict/aqi/{city}")
def predict_aqi(city: str):
    result = get_aqi_prediction(city)
    return result


@router.get("/api/predict/stress/{city}")
def stress_prediction(city: str):
    result = get_city_stress(city)

    if result is None:
        return {"error": "City not found"}

    return result


@router.get("/api/predict/stress-ranking")
def stress_ranking():
    return get_stress_ranking()


@router.get("/api/predict/alerts")
def city_alerts():
    return get_city_alerts()
