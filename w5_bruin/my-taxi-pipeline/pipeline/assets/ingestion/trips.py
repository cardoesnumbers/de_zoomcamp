"""@bruin
name: ingestion.trips
type: python
image: python:3.11
connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the meter was engaged"
  - name: dropoff_datetime
    type: timestamp
    description: "When the meter was disengaged"
@bruin"""

import os
import json
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month:02d}.parquet"


def materialize():
    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]
    taxi_types = json.loads(os.environ["BRUIN_VARS"]).get("taxi_types", ["yellow"])

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    frames = []
    for taxi_type in taxi_types:
        current = start.replace(day=1)
        end_month = end.replace(day=1)
        while current <= end_month:
            url = BASE_URL.format(
                taxi_type=taxi_type,
                year=current.year,
                month=current.month,
            )
            try:
                df = pd.read_parquet(url)
                df["taxi_type"] = taxi_type
                frames.append(df)
            except Exception:
                # Skip missing months (e.g. future or not yet published)
                pass
            current += relativedelta(months=1)

    if not frames:
        return pd.DataFrame(columns=["pickup_datetime", "dropoff_datetime"])
    final_dataframe = pd.concat(frames, ignore_index=True)
    return final_dataframe