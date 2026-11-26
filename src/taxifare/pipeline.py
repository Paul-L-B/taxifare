"""Custom functions used by the TaxiFare preprocessing pipeline."""
import math

import numpy as np
import pandas as pd

# Constants taken from the data scientist's notebook.
TIMEDELTA_MIN = 0
TIMEDELTA_MAX = 2190  # the model may extend in the future; slightly >1.0 after scaling is fine
LONLAT_FEATURES = [
    "pickup_latitude",
    "pickup_longitude",
    "dropoff_latitude",
    "dropoff_longitude",
]


def manhattan_distance_vectorized(
    df: pd.DataFrame, start_lat: str, start_lon: str, end_lat: str, end_lon: str
) -> pd.Series:
    """Manhattan distance in km between two points given in decimal degrees.

    Vectorized version for a pandas DataFrame.
    """
    earth_radius = 6371

    lat_1_rad, lon_1_rad = np.radians(df[start_lat]), np.radians(df[start_lon])
    lat_2_rad, lon_2_rad = np.radians(df[end_lat]), np.radians(df[end_lon])

    dlon_rad = lon_2_rad - lon_1_rad
    dlat_rad = lat_2_rad - lat_1_rad

    manhattan_rad = np.abs(dlon_rad) + np.abs(dlat_rad)
    return manhattan_rad * earth_radius


def scale_passenger(p):
    """Min-max scale the passenger count (range 0 to 8)."""
    p_min = 0.0
    p_max = 8.0
    return (p - p_min) / (p_max - p_min)


def transform_time_features(X: pd.DataFrame) -> pd.DataFrame:
    """Build time features from ``pickup_datetime``.

    Returns cyclical hour and month encodings, the day of week and the
    number of days since 2009-01-01 (``timedelta``).
    """
    if isinstance(X, pd.Series):
        X = X.to_frame()

    pickup_dt = pd.to_datetime(X["pickup_datetime"], utc=True)
    timedelta = (
        pickup_dt - pd.Timestamp("2009-01-01T00:00:00", tz="UTC")
    ) / pd.Timedelta(1, "D")

    pickup_dt_ny = pickup_dt.dt.tz_convert("America/New_York").dt

    dow = pickup_dt_ny.weekday
    hour = pickup_dt_ny.hour
    month = pickup_dt_ny.month

    hour_sin = np.sin(2 * math.pi / 24 * hour)
    hour_cos = np.cos(2 * math.pi / 24 * hour)

    month_sin = np.sin(2 * math.pi / 12 * month)
    month_cos = np.cos(2 * math.pi / 12 * month)

    return pd.DataFrame(
        {
            "hour_sin": hour_sin,
            "hour_cos": hour_cos,
            "day_of_week": dow,
            "month_sin": month_sin,
            "month_cos": month_cos,
            "timedelta": timedelta,
        },
        index=X.index,
    )


def scale_timedelta(timedelta):
    """Min-max scale the ``timedelta`` feature."""
    return (timedelta - TIMEDELTA_MIN) / (TIMEDELTA_MAX - TIMEDELTA_MIN)


def manhattan_distance_for_pipe(df: pd.DataFrame) -> pd.DataFrame:
    """Manhattan distance (km) as a one-column DataFrame, for the pipeline."""
    distance = manhattan_distance_vectorized(df, *LONLAT_FEATURES)
    return pd.DataFrame({"distance": distance})


def scale_distance(dist):
    """Min-max scale the distance (range 0 to 100 km)."""
    dist_min = 0
    dist_max = 100
    return (dist - dist_min) / (dist_max - dist_min)
