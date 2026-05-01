# Week 6: Batch/Spark

Overall a shorter module that gave me a better picture of how massive (and flexible) Spark is.

This module covered Spark internals; how processes like Group by or Joins work and we got an overview of RDD. From the module I get a reference of when to add Spark to my workflow: if I doing ETL on **huge** amounts of data, by the tera or even petabytes; data aggregation (e.g., group by), joins or deduplication, or incremental loads on billions of rows, or in other words, the work doesn't fit into memory and Pandas cannot help.

## Module comments

- Alexei's explaining some of the challenges of reading csv vs parquet or what lazy and eager processes was great. Other nice real world examples were the workaround to getting the schemas using Pandas when reading csv files as, unlike parquet files, csv do not carry this information by default; similarly, what I thought was a clever use of sets to identify the interception of columns, that is columns that appear in both the green and the yellow dataset.
- One final "hands-on" solution was the simple approach to dealing with columns having different names in two otherwise identical datasets (tpep and lpep columns), which was just to rename them, who would have thought!
  - df.withColumnRename('lpep_pickup_datetime', 'pickup_datetime') \
  - df.withColumnRename('lpep_dropoff_datetime', 'dropoff_datetime') and then the same for the green one
- A common error I kept falling for was defining df = ... keeping the .show() at the end which caused errors down the line for instance when doing joins.
- Connecting Spark to BigQuery was just overwhelming but that is maybe because I find it to cumbersome to deal with all the credentials part in any platform but felt tools used in previous modules like dbt and Bruin made this process easier.



## Homework

As tradition, I indicate my answer with 👈 and compare with the actual answer from the cohort using ✅ if my answer was correct or ❗ if wrong.

### Question 1: Install Spark and PySpark

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?

```python
import pyspark

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

26/04/23 22:05:59 WARN Utils: Your hostname, debian resolves to a loopback address: 127.0.1.1; using 192.168.8.8 instead (on interface wlp2s0)
26/04/23 22:05:59 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/04/23 22:05:59 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable

spark.version
'3.5.1'

```


### Question 2: Yellow November 2025

Read the November 2025 Yellow into a Spark Dataframe.

Repartition the Dataframe to 4 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- 6MB
- 25MB 👈✅ 
- 75MB
- 100MB


~~~python
# reading the parquet file
url = '/home/carlos/Dokument/GitHub/de_zoomcamp/w6_batch/code/data/yellow_tripdata_2025-11.parquet'

df = spark.read.parquet(url)

#repartitioning the dataframe to 4 partitions
df = df.repartition(4)
~~~

~~~bash
(base) carlos@debian:~/Dokument/GitHub/de_zoomcamp/w6_batch/code/data/yellow$ ls -lh
totalt 98M
-rw-r--r-- 1 carlos carlos 25M 28 apr 19.02 part-00000-767ffdec-c700-4e06-82cd-03fcb2fad50a-c000.snappy.parquet
-rw-r--r-- 1 carlos carlos 25M 28 apr 19.02 part-00001-767ffdec-c700-4e06-82cd-03fcb2fad50a-c000.snappy.parquet
-rw-r--r-- 1 carlos carlos 25M 28 apr 19.02 part-00002-767ffdec-c700-4e06-82cd-03fcb2fad50a-c000.snappy.parquet
-rw-r--r-- 1 carlos carlos 25M 28 apr 19.02 part-00003-767ffdec-c700-4e06-82cd-03fcb2fad50a-c000.snappy.parquet
-rw-r--r-- 1 carlos carlos   0 28 apr 19.02 _SUCCESS
~~~


### Question 3: Count records

How many taxi trips were there on the 15th of November?

Consider only trips that started on the 15th of November.

- 62,610
- 102,340
- 162,604 👈✅
- 225,768

Tried two approaches for this one, using pyspark sql functions with between and  using built logical operators:

### Option 1

~~~python
from pyspark.sql.functions import col

trip_count = df.filter(col('tpep_pickup_datetime').between('2025-11-15 00:00:00', '2025-11-15 23:59:59')).count()
print(f"Number of trips on November 15th: {trip_count}")

Number of trips on November 15th: 162604
~~~

### Option 2

~~~python
count_trip = df.filter((df.tpep_pickup_datetime >= '2025-11-15 00:00:00') & (df.tpep_pickup_datetime < '2025-11-16 00:00:00')).count()
print(f"Count of trips on November 15th: {count_trip}")

Count of trips on November 15th: 162604
~~~

### Question 4: Longest trip

What is the length of the longest trip in the dataset in hours?

- 22.7
- 58.2
- 90.6 👈✅
- 134.5

**Steps followed here**:
1. Imported pyspark.sql functions
2. Created a new df with just pickup and dropoff times
3. Converted both dropoff and pickup columns to seconds since epoch using [unix_timestamp](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.unix_timestamp.html) and substracted those two values to create a new column in the dataframe called 'time_length'.
4. Converted the resulting seconds to hours.

Final code snippet looks like this:

~~~python
df_time \
    .select(
        'trip_length', 
        F.round(F.col('trip_length')/3600, 2).alias('trip_hours')) \
    .orderBy(F.col('trip_length').desc()) \
    .show(5)

[Stage 109:>                                                        (0 + 4) / 4]
+-----------+----------+
|trip_length|trip_hours|
+-----------+----------+
|     326328|     90.65|
|     277014|     76.95|
|     274370|     76.21|
|     249439|     69.29|
|     241490|     67.08|
+-----------+----------+
only showing top 5 rows
~~~

More examples of using unix_timestamp can be found [here](https://statistics.arabpsychology.com/pyspark-calculate-a-difference-between-two-dates/).


### Question 5: User Interface

Spark's User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040 👈✅
- 8080

It runs in http://localhost:4040/jobs/

~~~markdown
Spark Jobs (?)
User: carlos
Total Uptime: 47,8 h
Scheduling Mode: FIFO
Completed Jobs: 67
~~~

### Question 6: Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark:

```bash
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Using the zone lookup data and the Yellow November 2025 data, what is the name of the LEAST frequent pickup location Zone?

- Governor's Island/Ellis Island/Liberty Island 👈✅
- Arden Heights 👈✅
- Rikers Island
- Jamaica Bay

If multiple answers are correct, select any

**Steps**:
1. Read the zones file as df, the file already downloaded when doing the setup for PySpark.
2. Join them, set truncate to False to get the full name of the zone

~~~python
#File already downloaded in the setup step
url = "/home/carlos/Dokument/GitHub/de_zoomcamp/w6_batch/00_setup/taxi_zone_lookup.csv"
zone_df = spark.read.option("header", "true").csv(url)
~~~

~~~python
# name of the LEAST frequent pickup location ID just from the november data
least_freq_pickup_zone = df.groupBy('PULocationID').count().orderBy('count')
least_freq_pickup_zone.show(5, truncate = False)

+------------+-----+
|PULocationID|count|
+------------+-----+
|84          |1    |
|105         |1    |
|5           |1    |
|187         |3    |
|111         |4    |
+------------+-----+
only showing top 5 rows
~~~

~~~python
# joining with the zone dataframe to get the zone names
df.join(zone_df, df.PULocationID == zone_df.LocationID, 'left') \
.groupBy(['LocationID', 'Zone'])\
.count().orderBy('count').show(5, truncate = False)

+----------+---------------------------------------------+-----+
|LocationID|Zone                                         |count|
+----------+---------------------------------------------+-----+
|105       |Governor's Island/Ellis Island/Liberty Island|1    |
|84        |Eltingville/Annadale/Prince's Bay            |1    |
|5         |Arden Heights                                |1    |
|187       |Port Richmond                                |3    |
|199       |Rikers Island                                |4    |
+----------+---------------------------------------------+-----+
only showing top 5 rows

~~~