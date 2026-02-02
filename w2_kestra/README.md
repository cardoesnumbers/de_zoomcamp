# Module Comments


Finally got to Kestras login page. The main issue preventing this was localhost:8080 is not compatible with they way Github Codespaces work. Basically:

- The Docker container is running inside a remote VM
- You need to use the forwarded port URL, not localhost. 
- The login URL is the name of my codespaces + a bunch of numbers + .app.github.dev/ui/login?from=/dashboards
- The actual URL could have been checked earlier looking at the PORTS menu :)
- I guess the intention was to run this locally?

I also had the original docker compose file in the same folder, even with a different name (but same extension) it seemsd to be causing some confusion when running the docker compose up command. At the end I changed the extension to .bak 


After checking best practices I am sticking to develop locally which SIGNIFICANTLY reduced the setup time.


On the schedule section, I don't remmeber it being mentioned in the training video but executing the flow when the trigger details are not current (cron) would result in a FAILED at the very first task (labeling). As suggested in the video, what it can be done is to work with a backfill to get the data flowing




# Homework


## 1. Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?

128.3 MiB
Had to download the extracted file from the outputs but there seems to be some tasks I can add to the flow after the Extract task to get it, example to see it logs: 

     id: get_file_info
    type: io.kestra.plugin.scripts.shell.Commands
    commands:
    - ls -lh {{outputs.extract.outputFiles[inputs.taxi ~ '_tripdata_' ~ (trigger.date | date('yyyy-MM')) ~ '.csv']}}
    - du -h {{outputs.extract.outputFiles[inputs.taxi ~ '_tripdata_' ~ (trigger.date | date('yyyy-MM')) ~ '.csv']}}
  

## 2. What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?

    green_tripdata_2020-04.csv

By just replacing the corresponding values in: 

    variables:

    file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"



For the following three questions I ran a backfill in Kestra from Jan 1, 2020 to April 1, 2021 both dates at 00:00:00 to capture the full days


## 3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?

    13,537.299
    24,648,499 <<<
    18,324,219
    29,430,127

My result doesnt match any of the options, initial query resulted in 13,537,299 but it seems the flow is still running, as got 19 and the 20 millions on subsequent queries. Seems to have settled at 24,648,235

SQL: SELECT 
COUNT(*) 
FROM public.yellow_tripdata_345
WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2020;

## 4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?

    5,327,301
    936,199
    1,734,051 <<<
    1,342,034

This one was closer, 1,733,999 

SELECT 
COUNT(*) 
FROM public.green_tripdata_345
WHERE EXTRACT(YEAR FROM lpep_pickup_datetime) = 2020;

## 5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

    1,428,092
    706,911
    1,925,152 <<<
    2,561,031

Also a close one: 1,925,121

SELECT COUNT(*) FROM public.yellow_tripdata_345
WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2021
  AND EXTRACT(MONTH FROM tpep_pickup_datetime) = 3;

## 6. How would you configure the timezone to New York in a Schedule trigger?

    Add a timezone property set to America/New_York in the Schedule trigger configuration
 
    Timezones not covered in the videos but based on the documentation:
    https://kestra.io/plugins/core/trigger/io.kestra.plugin.core.trigger.schedule#properties_timezone-body  and
    https://en.wikipedia.org/wiki/List_of_tz_database_time_zones


