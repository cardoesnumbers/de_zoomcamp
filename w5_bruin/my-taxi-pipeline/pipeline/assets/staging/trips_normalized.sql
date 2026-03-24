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

-- Raw ingestion keeps TLC column names (yellow: tpep_*, green: lpep_*). Unify here.
SELECT
  COALESCE(
    CAST(t.tpep_pickup_datetime AS TIMESTAMP),
    CAST(t.lpep_pickup_datetime AS TIMESTAMP)
  ) AS pickup_datetime,
  COALESCE(
    CAST(t.tpep_dropoff_datetime AS TIMESTAMP),
    CAST(t.lpep_dropoff_datetime AS TIMESTAMP)
  ) AS dropoff_datetime,
  CAST(t.pu_location_id AS INTEGER) AS pickup_location_id,
  CAST(t.do_location_id AS INTEGER) AS dropoff_location_id,
  CAST(t.payment_type AS INTEGER) AS payment_type,
  CAST(t.fare_amount AS DOUBLE) AS fare_amount,
  -- Backfill: append-only ingestion can leave NULL on older rows (added column later);
  -- TLC files never carry this — yellow uses tpep_*, green uses lpep_*.
  COALESCE(
    t.taxi_type,
    CASE
      WHEN t.tpep_pickup_datetime IS NOT NULL THEN 'yellow'
      WHEN t.lpep_pickup_datetime IS NOT NULL THEN 'green'
    END
  ) AS taxi_type
FROM ingestion.trips AS t
WHERE COALESCE(
    CAST(t.tpep_pickup_datetime AS TIMESTAMP),
    CAST(t.lpep_pickup_datetime AS TIMESTAMP)
  ) >= '{{ start_datetime }}'
  AND COALESCE(
    CAST(t.tpep_pickup_datetime AS TIMESTAMP),
    CAST(t.lpep_pickup_datetime AS TIMESTAMP)
  ) < '{{ end_datetime }}'
