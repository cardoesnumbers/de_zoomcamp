# Week 5: Data Platforms and Bruin

## Module Comments and Homework

**Tech**: [Bruin](https://getbruin.com/), [DuckDB](https://duckdb.org/), [Cursor](https://cursor.com/)

Just went through the Bruin playlist reviewing some of the features and capabilities Bruin has to offer. Very first impression is that it reminded me of dbt probably because of the work being yml-driven and the approach to seeds. I am taking the opportunity in this module to try out Cursor, MCP, and DuckDB.  

Ok, on to it. 

- The initial setup had duckdb installed to run with the module so I had a chance to do a quick check on it (almost entirely in the ui and only a few tests with cli). I thought it looked great, it felt light-weight despite all the features, and user friendly.  As I said after W4, I look forward to continue learning more about it.

- Linked to duckdb, because the .db file was also created locally I had to play around with Git/Github as [there is a limit of 100MB](https://github.com/orgs/community/discussions/163795) when doing regular commits. At the end, I used Git Large File Storage extension and everything seemed to work just fine. Also this was the first time I heard about LFS, so, great find.

For more about LFS read [here](https://git-lfs.com/)

- Working with Cursor was nice, particularly when generating the ingestion script which reminded me how much time I spent on that in W3. Code generation was amazing but also minimizes then chances of failing and learning from understanding (or at least trying to understand) what and why something is failing. I will probably use it in the next module though I am already quite comfortable with VS Code. Still, great to see suggestions like how to handle the pickup and dropoff column names in staging using COALESCE


~~~sql
SELECT
  COALESCE(
    CAST(t.tpep_pickup_datetime AS TIMESTAMP),
    CAST(t.lpep_pickup_datetime AS TIMESTAMP)
  ) AS pickup_datetime,
  COALESCE(
    CAST(t.tpep_dropoff_datetime AS TIMESTAMP),
    CAST(t.lpep_dropoff_datetime AS TIMESTAMP)
  ) AS dropoff_datetime,
~~~



## Homework

As in the previous module, I am no longer able to submit this but I will be replying to this answer and then commenting vs the correct answer provided in the repo

### Question 1. Bruin Pipeline Structure

In a Bruin project, what are the required files/directories?

- `bruin.yml` and `assets/`
- `.bruin.yml` and `pipeline.yml` (assets can be anywhere)
- `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/` ❗
- `pipeline.yml` and `assets/` only ☑️

**Comment**: I chose the third one based on the video lectures and class notes (02-Getting started > Project skeleton) but the correct answer is the last one. So, no .bruin.yml? This one was also interesting as I double checked with the chat/MCP and the answer was the third one as well and I assumed the MCP provided some context based on Bruins documentation. Then again MCP is new to me and maybe that's not how it works. 

### Question 2. Materialization Strategies

You're building a pipeline that processes NYC taxi data organized by month based on pickup_datetime. Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period?

- `append` - always add new rows
- `replace` - truncate and rebuild entirely
- `time_interval` - incremental based on a time column ☑️
- `view` - create a virtual table only

**Comment:** This was the correct answer, as indicated in the Zoomcamp template shared by Bruin and Choosing the right incremental key. More on Best Practices at https://github.com/bruin-data/bruin/tree/main/templates/zoomcamp 

### Question 3. Pipeline Variables

You have the following variable defined in pipeline.yml:

```yaml
variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
```

How do you override this when running the pipeline to only process yellow taxis?

- `bruin run --taxi-types yellow`
- `bruin run --var taxi_types=yellow`
- `bruin run --var 'taxi_types=["yellow"]'` ☑️
- `bruin run --set taxi_types=["yellow"]`❗

**Comment**: Third option was the correct one, I chosen the fourth one. Bruin documentation on variables verifies --var 'taxi_types=["yellow"] is the way. Check Overriding Variables at Runtime at https://getbruin.com/docs/bruin/core-concepts/variables.html  

### Question 4. Running with Dependencies

You've modified the ingestion/trips.py asset and want to run it plus all downstream assets. Which command should you use?

- `bruin run ingestion.trips --all`
- `bruin run ingestion/trips.py --downstream` ☑️
- `bruin run pipeline/trips.py --recursive`
- `bruin run --select ingestion.trips+` ❗

**Comment**: From the video lectures and I remembered the plus sign meaning to run the asset and its dependecies but the more I think about it I think that was from the dbt sessions. Anyway ther doesnt seem to be a "--all" flag for run or "--recursive". More info here: https://getbruin.com/docs/bruin/commands/run.html 

### Question 5. Quality Checks

You want to ensure the pickup_datetime column in your trips table never has NULL values. Which quality check should you add to your asset definition?

- `name: unique`
- `name: not_null` ☑️
- `name: positive`
- `name: accepted_values, value: [not_null]` 

**Comment**: This is correct, coming from the Zoomcamp template and available checks explanation from https://getbruin.com/docs/bruin/quality/available_checks.html#not-null

### Question 6. Lineage and Dependencies

After building your pipeline, you want to visualize the dependency graph between assets. Which Bruin command should you use?

- `bruin graph`
- `bruin dependencies`
- `bruin lineage` ☑️
- `bruin show`

Comment: This is correct. Based on trial and error and the information from https://getbruin.com/docs/bruin/commands/lineage.html resulting in:

~~~bash
bruin lineage pipeline/assets/staging/trips_normalized.sq
l

Lineage: 'staging.trips_normalized'

Upstream Dependencies
========================
- ingestion.trips (assets/ingestion/trips.py)

Total: 1
~~~

### Question 7. First-Time Run

You're running a Bruin pipeline for the first time on a new DuckDB database. What flag should you use to ensure tables are created from scratch?

- `--create`
- `--init`
- `--full-refresh` ☑️
- `--truncate`

**Comment**: This is correct. The documentation reads: "When running assets with the --full-refresh flag, Bruin will drop and recreate tables to ensure a clean state." or "Let's say you want to create a new table to track product catalog with SCD2. If the table doesn't exist yet, you'll need an initial run with the --full-refresh flag:

~~~bash
bruin run --full-refresh path/to/your/product_catalog.sql
~~~

When using `time_interval` strategy, the `incremental_key` determines which rows to delete and re-insert during each run".

More info on --full-refresh: https://getbruin.com/docs/bruin/assets/materialization.html#full-refresh-and-refresh-restricted 

