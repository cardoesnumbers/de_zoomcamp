/* @bruin
name: staging.trips_normalized
type: duckdb.sql
connection: duckdb-default

depends:
  - ingestion.trips

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp

columns:
  - name: pickup_datetime
    type: timestamp
    checks:
      - name: not_null
@bruin */

SELECT
  CAST(t.tpep_pickup_datetime AS TIMESTAMP) AS pickup_datetime,
  CAST(t.tpep_dropoff_datetime AS TIMESTAMP) AS dropoff_datetime,
  CAST(t.PULocationID AS INTEGER) AS pickup_location_id,
  CAST(t.DOLocationID AS INTEGER) AS dropoff_location_id,
  CAST(t.payment_type AS INTEGER) AS payment_type,
  CAST(t.fare_amount AS DOUBLE) AS fare_amount,
  t.taxi_type AS taxi_type
FROM ingestion.trips AS t
WHERE CAST(t.tpep_pickup_datetime AS TIMESTAMP) >= '{{ start_datetime }}'
  AND CAST(t.tpep_pickup_datetime AS TIMESTAMP) < '{{ end_datetime }}'
