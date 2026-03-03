from fastapi import APIRouter
from app.services.data_loader import load_city_snapshot
from app.services.analytics_service import generate_alerts

router = APIRouter()


@router.get("/api/alerts")
def get_alerts():
    df = load_city_snapshot()
    alerts = generate_alerts(df)

    return {"total_alerts": len(alerts), "alerts": alerts}
