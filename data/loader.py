import pandas as pd
import numpy as np
import os

def load_nyc_taxi_data(n_rows: int = 5000) -> pd.DataFrame:
    """
    Loads NYC taxi data. Tries public parquet first, falls back to synthetic.
    """
    cache_path = "data/nyc_taxi_sample.parquet"

    if os.path.exists(cache_path):
        return pd.read_parquet(cache_path)

    try:
        url = (
            "https://d37ci6vzurychx.cloudfront.net/trip-data/"
            "yellow_tripdata_2024-01.parquet"
        )
        df = pd.read_parquet(url)
        df = df.sample(n=min(n_rows, len(df)), random_state=42).reset_index(drop=True)
        df = _clean(df)
        df.to_parquet(cache_path, index=False)
        return df
    except Exception:
        return _generate_synthetic(n_rows)


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    rename = {
        "tpep_pickup_datetime": "pickup_datetime",
        "tpep_dropoff_datetime": "dropoff_datetime",
        "trip_distance": "trip_distance",
        "fare_amount": "fare_amount",
        "tip_amount": "tip_amount",
        "total_amount": "total_amount",
        "passenger_count": "passenger_count",
        "PULocationID": "pickup_location_id",
        "DOLocationID": "dropoff_location_id",
        "payment_type": "payment_type",
    }
    cols = [c for c in rename if c in df.columns]
    df = df[cols].rename(columns=rename)

    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
    df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"], errors="coerce")
    df = df.dropna(subset=["pickup_datetime", "fare_amount"])

    df["hour"] = df["pickup_datetime"].dt.hour
    df["day_of_week"] = df["pickup_datetime"].dt.day_name()
    df["trip_duration_min"] = (
        (df["dropoff_datetime"] - df["pickup_datetime"]).dt.total_seconds() / 60
    ).round(2)
    df["speed_mph"] = (df["trip_distance"] / (df["trip_duration_min"] / 60)).round(2)
    df["tip_pct"] = ((df["tip_amount"] / df["fare_amount"]) * 100).round(2)

    # Remove bad rows
    df = df[
        (df["fare_amount"] > 0)
        & (df["trip_distance"] > 0)
        & (df["trip_duration_min"] > 0)
        & (df["trip_duration_min"] < 180)
        & (df["speed_mph"] < 100)
    ]
    return df.reset_index(drop=True)


def _generate_synthetic(n: int = 5000) -> pd.DataFrame:
    """Generate realistic synthetic NYC taxi data."""
    np.random.seed(42)
    rng = np.random

    # Peak hours: morning (7-9) and evening (17-19) commutes
    hour_weights = np.array([
        1, 0.5, 0.3, 0.3, 0.4, 0.8,
        1.5, 3.0, 3.5, 2.0, 1.5, 1.8,
        2.0, 1.8, 1.6, 1.5, 1.8, 3.2,
        3.5, 2.8, 2.5, 2.2, 1.8, 1.3,
    ])
    hour_weights /= hour_weights.sum()

    hours = rng.choice(24, size=n, p=hour_weights)
    days = rng.choice(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        size=n,
        p=[0.16, 0.16, 0.16, 0.15, 0.17, 0.12, 0.08],
    )

    trip_distance = np.abs(rng.lognormal(mean=1.0, sigma=0.8, size=n)).clip(0.1, 30)
    trip_duration_min = (trip_distance * rng.uniform(3, 6, size=n)).clip(2, 120)
    speed_mph = (trip_distance / (trip_duration_min / 60)).round(2)
    fare_amount = (2.5 + trip_distance * 2.5 + rng.uniform(0, 3, size=n)).round(2)
    tip_pct = np.where(
        rng.random(n) < 0.85,
        rng.normal(loc=18, scale=5, size=n).clip(0, 50),
        0,
    )
    tip_amount = (fare_amount * tip_pct / 100).round(2)
    total_amount = (fare_amount + tip_amount + rng.uniform(0.5, 2, n)).round(2)
    passenger_count = rng.choice([1, 2, 3, 4, 5, 6], size=n, p=[0.55, 0.22, 0.10, 0.07, 0.04, 0.02])
    payment_type = rng.choice([1, 2, 3], size=n, p=[0.65, 0.30, 0.05])

    nyc_zones = list(range(1, 264))
    pickup_location_id = rng.choice(nyc_zones, size=n)
    dropoff_location_id = rng.choice(nyc_zones, size=n)

    base_date = pd.Timestamp("2024-01-01")
    pickup_datetime = [
        base_date
        + pd.Timedelta(days=int(rng.randint(0, 31)))
        + pd.Timedelta(hours=int(h))
        + pd.Timedelta(minutes=int(rng.randint(0, 60)))
        for h in hours
    ]
    dropoff_datetime = [
        p + pd.Timedelta(minutes=float(d))
        for p, d in zip(pickup_datetime, trip_duration_min)
    ]

    return pd.DataFrame({
        "pickup_datetime": pickup_datetime,
        "dropoff_datetime": dropoff_datetime,
        "trip_distance": trip_distance.round(2),
        "fare_amount": fare_amount,
        "tip_amount": tip_amount,
        "total_amount": total_amount,
        "passenger_count": passenger_count,
        "pickup_location_id": pickup_location_id,
        "dropoff_location_id": dropoff_location_id,
        "payment_type": payment_type,
        "hour": hours,
        "day_of_week": days,
        "trip_duration_min": trip_duration_min.round(2),
        "speed_mph": speed_mph,
        "tip_pct": tip_pct.round(2),
    })


def get_summary_stats(df: pd.DataFrame) -> dict:
    """Compute KPI summary stats for the crew agents."""
    return {
        "total_trips": len(df),
        "avg_fare": round(df["fare_amount"].mean(), 2),
        "avg_distance": round(df["trip_distance"].mean(), 2),
        "avg_duration_min": round(df["trip_duration_min"].mean(), 2),
        "avg_tip_pct": round(df["tip_pct"].mean(), 2),
        "avg_speed_mph": round(df["speed_mph"].mean(), 2),
        "total_revenue": round(df["total_amount"].sum(), 2),
        "peak_hour": int(df.groupby("hour")["trip_distance"].count().idxmax()),
        "busiest_day": df["day_of_week"].value_counts().idxmax(),
        "avg_passengers": round(df["passenger_count"].mean(), 2),
        "payment_split": df["payment_type"].value_counts(normalize=True).round(3).to_dict(),
        "fare_p25": round(df["fare_amount"].quantile(0.25), 2),
        "fare_p75": round(df["fare_amount"].quantile(0.75), 2),
        "long_trips_pct": round((df["trip_distance"] > 10).mean() * 100, 2),
        "high_tip_pct": round((df["tip_pct"] > 20).mean() * 100, 2),
    }
