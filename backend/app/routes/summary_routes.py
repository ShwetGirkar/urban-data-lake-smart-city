from fastapi import APIRouter
from app.services.data_loader import load_city_snapshot
from app.services.analytics_service import compute_summary

router = APIRouter()


@router.get("/api/summary")
def get_summary():
    df = load_city_snapshot()
    return compute_summary(df)
