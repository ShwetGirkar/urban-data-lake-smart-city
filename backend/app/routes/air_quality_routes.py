from fastapi import APIRouter
from app.services.aqi_service import get_air_quality_by_city

router = APIRouter()


@router.get("/api/air-quality/{city_name}")
def get_air_quality(city_name: str):
    result = get_air_quality_by_city(city_name)

    if result is None:
        return {"error": "City not found"}

    return result
