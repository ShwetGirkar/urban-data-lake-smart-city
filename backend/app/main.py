from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# import os
from fastapi import FastAPI
from app.routes import (
    city_routes,
    summary_routes,
    alerts_routes,
    air_quality_routes,
    traffic_routes,
    search_routes,
    prediction_routes,
)

load_dotenv()
app = FastAPI(title="Urban Data Lake API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(city_routes.router)
app.include_router(summary_routes.router)
app.include_router(alerts_routes.router)
app.include_router(air_quality_routes.router)
app.include_router(traffic_routes.router)
app.include_router(search_routes.router)
app.include_router(prediction_routes.router)


@app.get("/")
def root():
    return {"message": "Urban Data Lake Backend Running"}
