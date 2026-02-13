# Module 3: Data Warehouse (BigQuery, DuckDB) 
## Comments and Homework


### Module Comments

This module has been really tough to follow (right now using the dlt path). The main challenge is getting my head around dlt setup:
- becoming familiar with dlt commands, not really there yet.
- Dlt upload script ran into some misunderstandings regarding how GCP credentials were handled.
- Secrets management is pretty straight forward working in Colab and its already part of the GCP/Google ecosystem.
- Those issues with GCP credentials were luckily sorted out with the help of Gemini in Colab
- I was hoping an interface for DuckDB?

Was confused by not being able to find the rides dataset in BigQuery, turns out this should have been expected as I was following the course suggested ingestions steps and the first phase is to move the parquet to duckdb for testing (and later to BQ for prod)

When running the ingestion into BQ ran into a couple of errors which reminded I'd used a separate service account for the dlt/BigQuery module.

Forbidden: 403 POST: Access Denied: User does not have bigquery.jobs.create permission in project...

and 

Forbidden: 403 POST: Access Denied: User does not have permission to query table...

This was sorted out by granting this particular service account the needed permission.


## Homework

### BigQuery Setup

For this sections I have taken out the uris information for safety/security.

**Create an external table using the Yellow Taxi Trip Records.**

~~~~sql
CREATE OR REPLACE EXTERNAL TABLE
  `XXXX.rides_dataset.rides_external` 
    OPTIONS (
    format = 'PARQUET',
    uris = ['gs://XXXX']
  );
~~~~


**Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table).**

~~~~sql
CREATE OR REPLACE TABLE `XXXX.rides_dataset.rides_internal`
AS
SELECT * FROM `XXXX.rides_dataset.rides_external`;
~~~~



**Question 1. Counting records What is count of records for the 2024 Yellow Taxi Data?**

select
count(*)
from `rides_dataset.rides_internal`;

    65,623
    840,402
    20,332,093 <<<
    85,431,289




**Question 2. Data read estimation. Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?**

~~~~sql
select
count(distinct pu_location_id)
from
(select
  pu_location_id
  from `rides_dataset.rides_external` --just taking location col in the the external table
union all
select
  pu_location_id
  from `rides_dataset.rides_internal`); --just taking location col in the the external table
~~~~




    18.82 MB for the External Table and 47.60 MB for the Materialized Table
    0 MB for the External Table and 155.12 MB for the Materialized Table <<<
    2.14 GB for the External Table and 0MB for the Materialized Table
    0 MB for the External Table and 0MB for the Materialized Table

**Question 3. Understanding columnar storage. Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?**

    BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
    BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
    BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
    When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed

**Question 4. Counting zero fare trips. How many records have a fare_amount of 0?**

    128,210
    546,578
    20,188,016
    8,333

**Question 5. Partitioning and clustering**

What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

    Partition by tpep_dropoff_datetime and Cluster on VendorID
    Cluster on by tpep_dropoff_datetime and Cluster on VendorID
    Cluster on tpep_dropoff_datetime Partition by VendorID
    Partition by tpep_dropoff_datetime and Partition by VendorID

**Question 6. Partition benefits. Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive) Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.**

    12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
    310.24 MB for non-partitioned table and 26.84 MB for the partitioned table
    5.87 MB for non-partitioned table and 0 MB for the partitioned table
    310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

**Question 7. External table storage. Where is the data stored in the External Table you created?**

    Big Query
    Container Registry
    GCP Bucket
    Big Table

**Question 8. Clustering best practices. It is best practice in Big Query to always cluster your data:**

    True
    False

**Question 9. Understanding table scans. No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?**
