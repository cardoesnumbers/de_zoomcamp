# Week 5: Data Platforms and Bruin

## Module Comments and Homework

**Tech**: [Bruin](https://getbruin.com/), [DuckDB](https://duckdb.org/), [Cursor](https://cursor.com/)

### Quick Summary/Overview

This was a great intro to Bruin. I went through the Bruin playlist reviewing some of the features and capabilities Bruin has to offer. It reminded me of dbt probably because that was the previous module also the work being yml-driven or properly stated "version-controllable text", and the option of managing seeds. Videos were done using Cursor as IDE which is nice, I also wanted to tried it out together with MCP, and DuckDB.  

### In Bruin

- So, the work is done following a (suggested) **data design** patern diving the project assets in ingestion, staging, and reports; again just like we did in the previous module. Assets in each stage (of this project) were Python scripts, SQL code, or seeds. A difference on how the platform manages seeds is that the nature of the seed is declare in a yml file located next to it which allows it to be referenced in other steps. In dbt we ran "dbt seed" for to load them into the warehouse. 
  
- Really like the **Bruin render**/window (that comes with the extension?) which allows to adjust start and end dates for when the pipeline runs as well as visualizing code preview, schemas or adjusting checks for an specific asset. It is possible also to set those start and end date from terminal.
  
- Built-in **lineage** tab was also helpful visualizing dependencies at different stages or using **validate** before running a pipeline to check for errors in syntax or checks.

- The initial zoomcamp setup in Bruin had **duckdb** installed to run with the module so I had a chance to finally test it (almost entirely in the ui and only a few times from terminal). I thought it looked great, it felt light-weight despite all the features, and user friendly. During this module I skipped testing to move the data to BigQuery a combination of being tired to looking at it from W4 and just wanting to test duckdb more. Might try to do that sometime in the future. 
  
- Related to BG (and Looker), I will check what BI/viz tools have **DuckDB connectivity**.

- On version control, because the .db file was also created locally I had to play around with Git/Github as [there is a limit of 100MB](https://github.com/orgs/community/discussions/163795) when doing regular commits. At the end, I used Git Large File Storage extension and everything seemed to work just fine. Also this was the first time I heard about LFS, so, great find. Alternatively, I guess I could have just add *.db to the .gitignore. 

  For more about LFS read [here](https://git-lfs.com/)

- Working with Cursor was nice, particularly when generating the ingestion script which reminded me how much time I spent on that in W3. Code generation was impressive though I couldn't help feeling I missed chances to fail more and learn from understanding (or at least trying to understand) what and why something was failing? But I cannot deny it is a time saver e.g., handling pickup and dropoff column names (not the same for yellow and green) or taxi types (not present in the source) using COALESCE (see example below). 
  
  I will most likely use it in the next module but I'm still partial to VS Code. Similarly to the BigQuery comment, I wasn't too interested in seeing Cursor+MPC build the whole pipeline from scratch but it is great to know that is an option and that the Bruin team provided great guidelines on what to ask in order to make the best of it. 

  
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
- `pipeline.yml` and `assets/` only ✅

**Comment**: I chose the third one based on the video lectures and class notes (02-Getting started > Project skeleton) but the correct answer is the last one. So, no .bruin.yml? This one was also interesting as I double checked with the chat/MCP and the answer was the third one as well and I assumed the MCP provided some context based on Bruins documentation. Then again MCP is new to me and maybe that's not how it works. Edit: Probably not how it works "Bruin MCP allows you to extend your AI agents to analyze, understand, and build upon your data using Bruin CLI. It allows AI agents to query data, compare tables, ingest data, and build pipelines on them." from https://getbruin.com/docs/bruin/getting-started/bruin-mcp.html

### Question 2. Materialization Strategies

You're building a pipeline that processes NYC taxi data organized by month based on pickup_datetime. Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period?

- `append` - always add new rows
- `replace` - truncate and rebuild entirely
- `time_interval` - incremental based on a time column ✅
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
- `bruin run --var 'taxi_types=["yellow"]'` ✅
- `bruin run --set taxi_types=["yellow"]`❗

**Comment**: Third option was the correct one, I chosen the fourth one. Bruin documentation on variables verifies --var 'taxi_types=["yellow"] is the way. Check Overriding Variables at Runtime at https://getbruin.com/docs/bruin/core-concepts/variables.html  

### Question 4. Running with Dependencies

You've modified the ingestion/trips.py asset and want to run it plus all downstream assets. Which command should you use?

- `bruin run ingestion.trips --all`
- `bruin run ingestion/trips.py --downstream` ✅
- `bruin run pipeline/trips.py --recursive`
- `bruin run --select ingestion.trips+` ❗

**Comment**: From the video lectures and I remembered the plus sign meaning to run the asset and its dependecies but the more I think about it I think that was from the dbt sessions. Anyway ther doesnt seem to be a "--all" flag for run or "--recursive". More info here: https://getbruin.com/docs/bruin/commands/run.html 

### Question 5. Quality Checks

You want to ensure the pickup_datetime column in your trips table never has NULL values. Which quality check should you add to your asset definition?

- `name: unique`
- `name: not_null` ✅
- `name: positive`
- `name: accepted_values, value: [not_null]` 

**Comment**: This is correct, coming from the Zoomcamp template and available checks explanation from https://getbruin.com/docs/bruin/quality/available_checks.html#not-null

### Question 6. Lineage and Dependencies

After building your pipeline, you want to visualize the dependency graph between assets. Which Bruin command should you use?

- `bruin graph`
- `bruin dependencies`
- `bruin lineage` ✅
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
- `--full-refresh` ✅
- `--truncate`

**Comment**: This is correct. The documentation reads: "When running assets with the --full-refresh flag, Bruin will drop and recreate tables to ensure a clean state." or "Let's say you want to create a new table to track product catalog with SCD2. If the table doesn't exist yet, you'll need an initial run with the --full-refresh flag:

~~~bash
bruin run --full-refresh path/to/your/product_catalog.sql
~~~

When using `time_interval` strategy, the `incremental_key` determines which rows to delete and re-insert during each run".

More info on --full-refresh: https://getbruin.com/docs/bruin/assets/materialization.html#full-refresh-and-refresh-restricted 

