"""Custom functions used by the TaxiFare preprocessing pipeline."""
import numpy as np
import pandas as pd


def scale_distance(X):
    """Scale the distance feature (divide by a typical trip distance)."""
    return X / 10.0


def scale_passenger(X):
    """Scale the passenger count feature."""
    return X / 6.0


def scale_timedelta(X):
    """Scale the time delta feature (days since a reference date)."""
    return X / 3000.0


def manhattan_distance_for_pipe(X: pd.DataFrame) -> pd.DataFrame:
    """Compute the Manhattan distance (in km) between pickup and dropoff.

    Args:
        X: DataFrame with pickup/dropoff longitude and latitude columns.

    Returns:
        DataFrame with one column, ``manhattan_distance``.
    """
    lat_km = 111.0
    lon_km = 111.0 * np.cos(np.radians(40.75))
    dlat = (X["dropoff_latitude"] - X["pickup_latitude"]).abs() * lat_km
    dlon = (X["dropoff_longitude"] - X["pickup_longitude"]).abs() * lon_km
    return pd.DataFrame({"manhattan_distance": dlat + dlon}, index=X.index)


def transform_time_features(X: pd.DataFrame) -> pd.DataFrame:
    """Extract time features from ``pickup_datetime``.

    Args:
        X: DataFrame with a ``pickup_datetime`` column.

    Returns:
        DataFrame with hour, day of week, month and days since 2009-01-01.
    """
    dt = pd.to_datetime(X["pickup_datetime"], utc=True)
    dt = dt.dt.tz_convert("America/New_York").dt.tz_localize(None)
    timedelta = (dt - pd.Timestamp("2009-01-01")) / pd.Timedelta(days=1)
    return pd.DataFrame(
        {
            "hour": dt.dt.hour,
            "dow": dt.dt.weekday,
            "month": dt.dt.month,
            "timedelta": timedelta,
        },
        index=X.index,
    )