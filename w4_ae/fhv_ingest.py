import os
import dlt
import requests
import pandas as pd
from dlt.destinations import filesystem
from io import BytesIO

os.environ["DLT_CONFIG_DIR"] = "/home/carlos/.dlt"

#   NUMERIC_COLUMNS = ["pulocationid", "dolocationid", "sr_flag"]

@dlt.resource(
    name="fhv_taxis",
    write_disposition="append",
)
def fhv_resource(months):
    for month in months:
        file_url = (
            f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
            f"fhv/fhv_tripdata_2019-{month:02d}.csv.gz"
        )

        print(f"🔄 Downloading: 2019-{month:02d}...")

        try:
            response = requests.get(file_url, stream=True, allow_redirects=True, timeout=60)
            response.raise_for_status()

            raw_bytes = BytesIO(response.content)

            for chunk in pd.read_csv(
                raw_bytes, compression="gzip", chunksize=200_000, low_memory=False
            ):
                chunk.columns = [c.lower().strip() for c in chunk.columns]

                # Convert location IDs and sr_flag to STRING to avoid type conflicts
                for col in ["pulocationid", "dolocationid", "sr_flag"]:
                    if col in chunk.columns:
                        chunk[col] = chunk[col].astype(str)

                # # Keep schema stable across all chunks/files for parquet writer.
                # for col in NUMERIC_COLUMNS:
                #     if col in chunk.columns:
                #         chunk[col] = (
                #             pd.to_numeric(chunk[col], errors="coerce")
                #             .astype("float64")
                #         )

                yield chunk

        except Exception as e:
            print(f"⚠️ Error downloading {file_url}: {e}")
            continue


pipeline = dlt.pipeline(
    pipeline_name="fhv_pipeline",
    destination="bigquery",
    dataset_name="fhv_dataset",
)

if __name__ == "__main__":
    load_info = pipeline.run(
        fhv_resource(months=range(1, 13)),
        loader_file_format="parquet",
        staging=filesystem(bucket_url="gs://dezc-485312"),
        )

    print("✅ Load complete!")
    print(load_info)
