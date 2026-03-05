
# Week 4: Analytics Engineering (dbt)


## Module Notes

Landing on week 4.

**Tech**: Terraform, ~~Docker~~, Google Colab, GCP, dbt

Once done with W3 I destroyed the GCP bucket (and all datasets in them) before realizing we will be using them in this section. This time instead of working with the first half of 2024 rides, we will focus on full 2019-2020 data. 

On W3 I used dlt to upload the data to the bucket in the form of a consolidated table, that is 6 parquet files were added to the dataset and then dlt allowed me to query it as if it was one. I intend to reuse that code but adjusting (adding outer loops) it so that it takes on both years [2019,2020] and all the months [1,13]. 

*Update after 2-3 days of not getting this to work.*

Green taxi data was relatively easy to get back on BigQuery mainly because it is much smaller than the yellow taxi. I had use Colab to load it and tried to do the same with the yellow one, adjusting the source url and leaving mostly evertyhing else as it was (changed pipeline names and database). This resulted in crash after crash due to running out of RAM our the session just timing out due to how extense the yellow rides are. 

I was reluctant to move away from the notebook as I found its handling of secrets just so simple but because of the constant crashing and frustration I moved now to work on my computer that I am hoping has enough RAM (16GB) and wont time out as in Colab. 

Secrets are currently on a tolm file being referenced in the script. The script has gone to multple reviews by me, Claude, and right now Codex. So far data is streaming 2019-11 which hopefully means something is happening. We will see in a couple of hours.

*Update.*


It worked. So now both green and yellow data is in BigQuery. When reviewing the local setup by the instructor noticed a different approach which is converting the original csv.gz files to parquet, so something to try out next time.


## Setting up dbt


DBT setup when working with BigQuery/Cloud was not too complicated. It helps that it can take the service account keys directly and extract the necessary credentials for the project. There is also the option of using Git/Github or their own version control option to track the changes in the project. 

Lots of work has been done on dbt models folder is used as data design architecture (?), that is it is a place where we can explicitly allocate data based on how much work we have done preparing it; 
  - models/staging takes the data from the source as described in the sources.yaml file
  - modes/intermediate is used for what the intructor called it, cosmetic adjustments (in the course we actually prepare the data already in the staging folder)
  - models/mart is where we will put the data that is ready for consumption/analyics
  
Besides the models, we used the seeds folder to store a lookup table with taxi zones

Curious also to try out the VS Code extensions including the power user one.



## Homework

### Question 1. dbt Lineage and Execution

Given a dbt project with the following structure:

models/
├── staging/
│   ├── stg_green_tripdata.sql
│   └── stg_yellow_tripdata.sql
└── intermediate/
    └── int_trips_unioned.sql (depends on stg_green_tripdata & stg_yellow_tripdata)

If you run dbt run --select int_trips_unioned, what models will be built?

    stg_green_tripdata, stg_yellow_tripdata, and int_trips_unioned (upstream dependencies)
    Any model with upstream and downstream dependencies to int_trips_unioned
    int_trips_unioned only ✅
    int_trips_unioned, int_trips, and fct_trips (downstream dependencies)

### Question 2. dbt Tests

You've configured a generic test like this in your schema.yml:

columns:
  - name: payment_type
    data_tests:
      - accepted_values:
          arguments:
            values: [1, 2, 3, 4, 5]
            quote: false

Your model fct_trips has been running successfully for months. A new value 6 now appears in the source data.

What happens when you run dbt test --select fct_trips?

    dbt will skip the test because the model didn't change
    dbt will fail the test, returning a non-zero exit code ✅
    dbt will pass the test with a warning about the new value
    dbt will update the configuration to include the new value

### Question 3. Counting Records in fct_monthly_zone_revenue

After running your dbt project, query the fct_monthly_zone_revenue model.

What is the count of records in the fct_monthly_zone_revenue model?

    12,998
    14,120
    12,184 ✅
    15,421

### Question 4. Best Performing Zone for Green Taxis (2020)

Using the fct_monthly_zone_revenue table, find the pickup zone with the highest total revenue (revenue_monthly_total_amount) for Green taxi trips in 2020.

Which zone had the highest revenue?

    East Harlem North ✅
    Morningside Heights
    East Harlem South
    Washington Heights South

### Question 5. Green Taxi Trip Counts (October 2019)

Using the fct_monthly_zone_revenue table, what is the total number of trips (total_monthly_trips) for Green taxis in October 2019?

    500,234
    350,891 ✅
    384,624
    421,509

### Question 6. Build a Staging Model for FHV Data

Create a staging model for the For-Hire Vehicle (FHV) trip data for 2019.

    Load the FHV trip data for 2019 into your data warehouse
    Create a staging model stg_fhv_tripdata with these requirements:
        Filter out records where dispatching_base_num IS NULL
        Rename fields to match your project's naming conventions (e.g., PUlocationID → pickup_location_id)

What is the count of records in stg_fhv_tripdata?

    42,084,899
    43,244,693
    22,998,722
    44,112,187

For this question there was an additional challenge of fixing a mismatch in datatypes between months. It appears the pulocationid and dolocationid columns when not Nan are identified as int64 adn when NaN as doubles. PyArrow (which I learned run under the hood of dbt) cannot combine int64 and double into the same Parquet file because the data types must be identical for all row groups. A workaround was to declare the data type like this:

```python
NUMERIC_COLUMNS = ["pulocationid", "dolocationid", "sr_flag"]
```

and then later on

```python
for chunk in pd.read_csv(
                raw_bytes, compression="gzip", chunksize=200_000, low_memory=False
            ):
                chunk.columns = [c.lower().strip() for c in chunk.columns]

                # Keep schema stable across all chunks/files for parquet writer.
                for col in NUMERIC_COLUMNS:
                    if col in chunk.columns:
                        chunk[col] = (
                            pd.to_numeric(chunk[col], errors="coerce")
                            .astype("float64")
                        )

                yield chunk
```



