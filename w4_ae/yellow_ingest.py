import os
import dlt
import requests
import pandas as pd
from dlt.destinations import filesystem
from io import BytesIO


os.environ["DLT_CONFIG_DIR"] = "/home/carlos/.dlt"


@dlt.resource(
    name="yellow_taxis",
    write_disposition="append",  # Ser till att data staplas månad för månad
    #primary_key="vendor_id",     # Valfritt: Hjälper dlt att identifiera rader
)
def taxi_rides_resource(years, months):
    for year in years:
        for month in months:
            file_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{year}-{month:02d}.csv.gz"
            
            print(f"🔄 Streamar data från: {year}-{month:02d}...")
            
            try:
                # Vi använder chunksize för att aldrig överstiga RAM-gränsen
                # low_memory=False förhindrar gissningar av datatyper som kan bli fel
                with pd.read_csv(file_url, compression='gzip', chunksize=100000, low_memory=False) as reader:
                    for chunk in reader:
                        # Konvertera kolumnnamn till snake_case (best practice för BigQuery)
                        chunk.columns = [c.lower().strip() for c in chunk.columns]
                        
                        # Skicka datablock till dlt
                        yield chunk.to_dict(orient="records")
            except Exception as e:
                print(f"⚠️ Fel vid nedladdning av {file_url}: {e}")
                continue

# 2. Skapa pipelinen
pipeline = dlt.pipeline(
    pipeline_name="yellow_pipeline",
    destination="bigquery",
    dataset_name="yellow_dataset"
)

# 3. Kör laddningen
if __name__ == "__main__":
    # Vi kör för 2019 och 2020, alla månader
    years_to_load = [2019, 2020]
    months_to_load = range(1, 13)
    
    # Här aktiverar vi staging="filesystem" för att använda din GCS bucket
    # Det är kritiskt för prestandan vid 200M rader
    load_info = pipeline.run(
        taxi_rides_resource(years_to_load, months_to_load),
        loader_file_format="parquet",
        staging=filesystem(bucket_url="gs://dezc-485312")
    )
    
    print("✅ Laddning slutförd!")
    print(load_info)
