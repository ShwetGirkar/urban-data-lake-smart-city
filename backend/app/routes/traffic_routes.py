from fastapi import APIRouter
from app.services.traffic_service import get_traffic_by_city

router = APIRouter()


@router.get("/api/traffic/{city_name}")
def get_traffic(city_name: str):
    result = get_traffic_by_city(city_name)

    if result is None:
        return {"error": "City not found"}

    return result
