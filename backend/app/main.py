from fastapi import FastAPI
from app.routes import city_routes, summary_routes

app = FastAPI(title="Urban Data Lake API")

app.include_router(city_routes.router)
app.include_router(summary_routes.router)


@app.get("/")
def root():
    return {"message": "Urban Data Lake Backend Running"}
