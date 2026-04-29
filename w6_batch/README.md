# Week 6: Batch/Spark

This module covers how to use Spark or actually PySpark as part of our data engineering stack. I have used pandas before and while they are different tools there is a familiarity on how Spark or PySpark that makes me feel almost at home.


## Module comments

- installing
- reading csv vs reading parquet
- lazy vs eager processes
- workaround to finding the schemas using pandas when working with csv files!
- clever using sets to identify the interception of columns, that is columns that appear in both the green and the yellow dataset
  - set(df_green.columns) & set(df_yellow.columns)
- similar to a simple clever approach with the tpep and lpep columns, just rename them
  - df.withColumnRename('lpep_pickup_datetime', 'pickup_datetime') \
  - df.withColumnRename('lpep_dropoff_datetime', 'dropoff_datetime') and then the same for the green one
- sql in spark. I have been working (as in actual work) a lot with SQL lately
- connecting spark to bigquery


## Homework

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

Comments: 25MB, based on the source parque file from NYC website. 

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
- 162,604 👈
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
- 90.6 👈
- 134.5

Steps followed here:
1. Created a new df with just pickup and dropoff times
2. 

### Question 5: User Interface

Spark's User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040
- 8080



### Question 6: Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark:

```bash
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Using the zone lookup data and the Yellow November 2025 data, what is the name of the LEAST frequent pickup location Zone?

- Governor's Island/Ellis Island/Liberty Island
- Arden Heights
- Rikers Island
- Jamaica Bay

If multiple answers are correct, select any


