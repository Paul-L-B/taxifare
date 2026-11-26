"""
FastAPI application for serving the taxifare model.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    """Root endpoint returning a greeting."""
    return {"greeting": "hello"}
