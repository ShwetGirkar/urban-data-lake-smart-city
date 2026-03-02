from fastapi import APIRouter
from app.services.data_loader import load_city_snapshot
from app.services.analytics_service import enrich_city_data

router = APIRouter()


@router.get("/api/cities")
def get_cities():
    df = load_city_snapshot()
    df = enrich_city_data(df)

    return df[
        [
            "city",
            "lat",
            "lon",
            "temperature_c",
            "aqi",
            "congestion_ratio",
            "urban_stress_score",
            "risk_level",
        ]
    ].to_dict(orient="records")


@router.get("/api/city/{city_name}")
def get_city_detail(city_name: str):
    df = load_city_snapshot()
    df = enrich_city_data(df)

    # Clean city column
    df["city_clean"] = df["city"].str.strip().str.lower()

    city_name_clean = city_name.strip().lower()

    city_data = df[df["city_clean"] == city_name_clean]

    if city_data.empty:
        return {"error": "City not found"}

    result = city_data.iloc[0].to_dict()
    result.pop("city_clean", None)
    return result
