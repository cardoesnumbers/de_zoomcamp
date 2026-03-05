
# Week 4: Analytics Engineering (dbt)


## Module Notes

This module took me three weeks to complete due to a combination of life, stubborness, and just basically learning something new. 

**Tech**: Terraform, ~~Docker~~, Google Colab, GCP, dbt Cloud, Codex

## Bringing the data back

On W3 I used dlt to upload the data to the bucket in the form of a consolidated table, that is 6 parquet files were added to the dataset and then dlt allowed me to query it as if it was one. I intend to reuse that code but adjusting (adding outer loops) it so that it takes on both years [2019,2020] and all the months [1,13]. 

The green taxi dataset was relatively easy to on BigQuery,I used Colab and things went smoothly. I tried the same with the yellow one, adjusting the source url and leaving mostly evertyhing else as it was (changed pipeline names and database). This resulted in crash after crash due to running out of RAM or the session just timing out due to how huge the yellow dataset is. 

I was reluctant to move away from the notebook as I found its handling of secrets just so simple but because of the constant crashing and frustration I moved to work locally, with a bit more RAM than Colab. Secrets were placed on a tolm file being  which in turned was referenced in the ingestion script. 

When reviewing the local setup by Juan (module instructor) I noticed a different approach which I think was converting the original csv.gz files to parquet (?), so something to try out next time.


## Setting up dbt


DBT setup when working with BigQuery/Cloud was not too complicated. It helps that it can take the service account keys directly and extract the necessary credentials for the project. There is also the option of using Git/Github or their own version control option to track the changes in the project. 

Lots of work took place on dbt models, using them as data design architecture (?), that is, it is a place where we can explicitly allocate data based on how much work we have done preparing it; 
  - models/staging takes the data from the source as described in the sources.yaml file
  - modes/intermediate is used for what the intructor called, cosmetic adjustments (in the course we already prepared some of the data already in the staging folder)
  - models/mart is where we will put the data that is ready for consumption/analyics
  
Besides the models, we used the seeds folder to store a lookup table with taxi zones as well as ways of payment.

Some other standout thoughts:

- Jinja and the fair amount of it saves when writing the code. 
- dbt Studio worked fine but I look forward to testing dbt extensions in VS Code when working locally.


## Homework

Since this module took me two forevers to complete I was not able to submit by the deadline, but still here come my answers. I am checking my answer and then commenting if this was correct or wrong based on the corrected questions.

### Question 1. dbt Lineage and Execution

Given a dbt project with the following structure:

```
models/
├── staging/
│   ├── stg_green_tripdata.sql
│   └── stg_yellow_tripdata.sql
└── intermediate/
    └── int_trips_unioned.sql (depends on stg_green_tripdata & stg_yellow_tripdata)
```

If you run dbt run --select int_trips_unioned, what models will be built?

    stg_green_tripdata, stg_yellow_tripdata, and int_trips_unioned (upstream dependencies)
    Any model with upstream and downstream dependencies to int_trips_unioned
    int_trips_unioned only ✅
    int_trips_unioned, int_trips, and fct_trips (downstream dependencies)

**Check**: This was verified when running it in dbt and it is also the correct answer.

### Question 2. dbt Tests

You've configured a generic test like this in your schema.yml:
```yaml
columns:
  - name: payment_type
    data_tests:
      - accepted_values:
          arguments:
            values: [1, 2, 3, 4, 5]
            quote: false
```
Your model fct_trips has been running successfully for months. A new value 6 now appears in the source data. What happens when you run dbt test --select fct_trips?

    dbt will skip the test because the model didn't change
    dbt will fail the test, returning a non-zero exit code ✅
    dbt will pass the test with a warning about the new value
    dbt will update the configuration to include the new value

**Check**: This was correct, initially by gut feeling and then by reading more on tests.


### Question 3. Counting Records in fct_monthly_zone_revenue

After running your dbt project, query the fct_monthly_zone_revenue model.

What is the count of records in the fct_monthly_zone_revenue model?

    12,998
    14,120
    12,184 ✅⚠️
    15,421

**Check**: Not the same result but the closest I got (12,157) based on
~~~~sql
select
count(*)
from {{ref('fct_monthly_rev')}}
~~~~

### Question 4. Best Performing Zone for Green Taxis (2020)

Using the fct_monthly_zone_revenue table, find the pickup zone with the highest total revenue (revenue_monthly_total_amount) for Green taxi trips in 2020.

Which zone had the highest revenue?

    East Harlem North ✅
    Morningside Heights
    East Harlem South
    Washington Heights South

**Check:** This is the correct answer and what I got from:

~~~~sql
select 
pickup_zone,
max(revenue_monthly_total_amount) as highest_revenue
from {{ref('fct_monthly_rev')}}
where taxi_type = 'green' and revenue_month between '2020-01-01' and '2020-12-31'
group by 1
order by highest_revenue DESC
~~~~


### Question 5. Green Taxi Trip Counts (October 2019)

Using the fct_monthly_zone_revenue table, what is the total number of trips (total_monthly_trips) for Green taxis in October 2019?

    500,234
    350,891 
    384,624 ✅⚠️
    421,509

**Check:** Similar situation to Q3, not the same result (367,253). I could have easily chosen the 350k one as well. SQL:

~~~~sql
select
sum(total_monthly_trips) as total_oct_trips
from {{ref('fct_monthly_rev')}}
where taxi_type = 'green' and revenue_month between '2019-10-01' and '2019-10-31'
~~~~

### Question 6. Build a Staging Model for FHV Data

Create a staging model for the For-Hire Vehicle (FHV) trip data for 2019.

    Load the FHV trip data for 2019 into your data warehouse
    Create a staging model stg_fhv_tripdata with these requirements:
        Filter out records where dispatching_base_num IS NULL
        Rename fields to match your project's naming conventions (e.g., PUlocationID → pickup_location_id)

What is the count of records in stg_fhv_tripdata?

    42,084,899
    43,244,693 ✅
    22,998,722
    44,112,187

**Check:** For this question there was an additional challenge of fixing a mismatch in datatypes between months/chunks. It appears the pulocationid and dolocationid columns when not Nan are identified as int64 and when NaN as doubles. PyArrow (which I learned runs under the hood of dbt) cannot combine int64 and double into the same Parquet file because the data types of each column must be identical across the different files. A workaround was to declare the data type for those columns as string like this:

```python
  for col in ["pulocationid", "dolocationid", "sr_flag"]:
                    if col in chunk.columns:
                        chunk[col] = chunk[col].astype(str)



