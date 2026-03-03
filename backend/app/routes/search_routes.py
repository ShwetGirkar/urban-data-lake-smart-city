from fastapi import APIRouter, Query
from app.services.search_service import search_location

router = APIRouter()


@router.get("/api/search")
def search(query: str = Query(...)):
    result = search_location(query)

    if result is None:
        return {"error": "Location not found"}

    return result
