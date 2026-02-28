from fastapi import FastAPI

app = FastAPI(title="Urban Data Lake API")


@app.get("/")
def root():
    return {"message": "Urban Data Lake Backend Running"}
