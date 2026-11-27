"""
FastAPI application for serving the taxifare model.
"""
import pandas as pd
from fastapi import FastAPI

from taxifare.predict import load_model, predict

app = FastAPI()
model = load_model()


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
    """Prediction endpoint: returns the fare predicted by the trained pipeline."""
    data = pd.DataFrame(
        {
            "pickup_datetime": [pickup_datetime],
            "pickup_longitude": [pickup_longitude],
            "pickup_latitude": [pickup_latitude],
            "dropoff_longitude": [dropoff_longitude],
            "dropoff_latitude": [dropoff_latitude],
            "passenger_count": [passenger_count],
        }
    )
    prediction = predict(model, data)
    return {"fare": float(prediction[0])}
