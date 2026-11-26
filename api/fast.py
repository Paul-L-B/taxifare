"""
FastAPI application for serving the taxifare model.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    """Root endpoint returning a greeting."""
    return {"greeting": "hello"}


@app.get("/predict")
def get_prediction(
    pickup_datetime: str,
    pickup_longitude: float,
    pickup_latitude: float,
    dropoff_longitude: float,
    dropoff_latitude: float,
    passenger_count: int,
):
    """Dummy prediction endpoint: returns the number of passengers times 2.5."""
    return {"fare": passenger_count * 2.5}
