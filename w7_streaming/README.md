# Module 7 - Streaming

## Module comments and observations

This is the final module of the Data Engineering Zoomcamp.

Ingredients:
- Docker for Flink + adapters, Postgres/PgAdmin, Redpanda
- Python, psycopg2
- NYC Taxi Data
- Cursor 

Have to admit this module was quite daunting for the lack of a better word. I think the overall idea is simple enough, in streaming we work with a producer, one or multiple consumer and then considering with the possibility of storing and transforming the data somewhere. My struggle when working with streaming are the moving parts in the docker compose which I already reckon when looking at the homework. But practice makes comfortable I suppose. 


### Concepts to keep in mind
- **Data streaming:** exchanging of data in "real time".
- **Kafka cluster:** nodes/machines talking to each other in a network.
- **Producer:** the one posting the information, it talks in terms of events or messages.
- **Consumer:** the one subscribed to the information being posted. Multple consumers can be group under a same consumer group id to let Kafka know they are part of the same entity = msg can go either to either.
- **Topic:** A continous stream of events defined by user, key-values. A topic is stored in one node of a Kafka cluster.
- **Event/Msg:** a data point at a certain timestamp, a collection of events go into a topic which in turn are read by the (subscribed) consumers. Each event contains a message.
- **Message:** whats inside of the event, has three structures: key, value, timestamp.
- **Replication (factor):** duplication a topic in +1 node. A leader node is defined here as well +1 node follower. Producers and consumers talk to the node leader. If node leader dies, the cluster adjusts and moves to node follower without much interruption in the work producer and consumer are doing. Follower becomes a leader and any other free nodes become follower, and so on.
- **Retention:** how long the data will be retain by Kafka, it deletes the message older than the retention. 
- **Partitions:** what allows Kafka to stream, it is the number of parts in which we are dividing a topic. Partitions can be replicated across nodes meaning the consumer can speak with multiple nodes at the same time. But if we have 1 partition then only 1 consumer can read. If we have 2 partitions we could use 2 consumers, etc. If we have 2 partitions and 3 consumers only 2 consumers will work but the 3 could become active if any of the first 2 dies.
- **Offset:** which message to consume. There is an offset attached to each message: 0, 1, 2, 3... this information is sent to Kakfa and K is able to recognized, based on the consumer group id, which messages have been consumed by which consumer. The details are stored in an internal K topic called __consumer_offset in something like <consumer-group-id, topic, partition, offset>.
- **Auto.offset.reset (latest and earliest):** indicates to K how to react when a new consumer group id has been attached to it. Latest is the default meaning if a new consumer is attached I can only read from that latest msg onwards and not the messages from the start of the topic (earliest).
- **Akc-all:** defines the behavior of the producer after it has fired a msg. 0 means it doesnt care if the node it is sending the msg to has actually written to the node. 1 means the msg has to be written into the node, after that it returns a success into the producer. All means both leader node and follower nodes needs to have written into both logs and until then will the producers get a success message.
- **Logs:** How we store events in a topic.

The work at hand is to produce simulated real-live events using a producer, use Redpanda to simplify what Kafka would have done when making the data available to a consumer. Use Flink to do some group by preprocessing on the rides. Moving the data to a database (Postgres). 

### Why Kakfa/Redpanda?
- Reliability and robustness to the topic (replication).
- Scalability (partitioning).
- Flexibility when it comes to choosing the size/extent of the above.

We worked with serializers and deserializers to convert data in a format that is compatible with streaming. 


**Quick summary on when to use each one:**

| Aspect | Serializer | Deserializer |
| --- | --- | --- |
| Purpose | Python object → Bytes/String | Bytes/String → Python object |
| Used When | Sending data (e.g., Kafka producer) | Receiving data (e.g., Kafka consumer) |
| Example | json.dumps(obj).encode('utf-8') | Ride(**json.loads(data.decode('utf-8'))) |
| Kafka Role | value_serializer in KafkaProducer | value_deserializer in KafkaConsumer |

To avoid having to call up (de)serializers on multiple cells, definitions for each one have been saved on an py file named models which I will use in the exercise to call for all the needed imports and above-mentioned functions. Like this:

~~~python
from models import ride_deserializer, TaxiRide
~~~


## Creating the producer

- (notebook file)
- identify the parts of the event 
- create a class based on the anatomy of the event
- convert the event to a dictionary*
- convert the dictionary to a json string*
- define KafkaProducer including servers and topic name

* these steps are automated with a **serializer**

## Creating the consumer 
- (separate notebook but im guessing this doesn't mattered much)
- define the consumer including server and topic name are the same as in the producer and the value **deserializer**. In Kafka, deserializers are used in consumers to reconstruct objects from bytes (created by the serializer)
- psycopg2 to load data to Postgres


Kafka/Redpanda and Postgres speak different languages, one bytes/json and the other pure SQL so psycopg2 works as receiver and interpreter via a python script.

In this exercise I am using Postgres, I am curious to know if duckdb would work as well? But for the sake of the exercise I will keep Postgres. One small change is that I dont like to write sql queries in the command line so I added a pgadmin service to the docker compose file instead.

~~~yaml
  pgadmin:
    image: dpage/pgadmin4:9.4
    restart: on-failure
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@local.dev
      - PGADMIN_DEFAULT_PASSWORD=admin
    ports:
      - "5050:80"
    depends_on:
      - postgres
~~~

After starting the Postgres service I need to create a table to receive the data I am sending (rides). This table should have the same structure as my rides, in other words, this:

~~~python
#creating one event exemple using this class
ride = TaxiRide( #TaxiRide as in the class from the models
    PULocationID=1,
    DOLocationID=2,
    trip_distance=10.66,
    total_amount=15.66,
    tpep_pickup_datetime=1726339200000 # epoch milliseconds 
)
~~~

should be mirrored in postgres (or whatever other service I might use), like this:

~~~sql
CREATE TABLE processed_events (
    PULocationID INTEGER,
    DOLocationID INTEGER,
    trip_distance DOUBLE PRECISION,
    total_amount DOUBLE PRECISION,
    pickup_datetime TIMESTAMP
);
~~~

Once created I needed to make some adjustments in the consumer (new consumer file), the producer remains as it is. Once the setup is done I need to resend the events from the producer.

## Flink

Flink is as a platform that would allow us to preprocess some of the data (vs storaging and processing done by Kafka/Redpanda) before it is moved to x or y location, Flink is also capable of dealing with common challenges like eventual breaks in connection. Flink is usually built in clusters that are always listening to the streams. Flink takes care of the consumption part and again the producer remains as it is. To work with Flink I need to add it to the docker compose in two parts: 

- a job manager (deciding to which task manager each job goes) and, 
- a task manager (what is actually doing the processes). 

The actual setup for flink is done via:
- a flink-config (some config), 
- a pyprojectflink.toml (dependencies), and 
- a dockerfile where everything comes together.

After adding them to the docker compose I execute both of them. 

~~~bash
docker compose up jobmanager taskmanager
~~~

**Reminder:** Before trying to configure any type of aggregation in Flink I need to cancel any ongoing jobs. For the aggregation I create a new table in pgadmin.


### Additional notes
- Check on Confluent cloud, video is 3 years old, is it still relevant?


# Homework



## Question 1. Redpanda version

Run `rpk version` inside the Redpanda container:

```bash
docker exec -it w7_streaming-redpanda-1 rpk version
```

What version of Redpanda are you running?

This is the result I get:

~~~bash
rpk version: v25.3.9
Git ref:     836b4a36ef6d5121edbb1e68f0f673c2a8a244e2
Build date:  2026 Feb 26 07 48 21 Thu
OS/Arch:     linux/amd64
Go version:  go1.24.3

Redpanda Cluster
  node-1  v25.3.9 - 836b4a36ef6d5121edbb1e68f0f673c2a8a244e2
~~~

## Question 2. Sending data to Redpanda

Create a topic called `green-trips`:

```bash
docker exec -it w7_streaming-redpanda-1 rpk topic create g_rides
```

Now write a producer to send the green taxi data to this topic.

Read the parquet file and keep only these columns:

- `lpep_pickup_datetime`
- `lpep_dropoff_datetime`
- `PULocationID`
- `DOLocationID`
- `passenger_count`
- `trip_distance`
- `tip_amount`
- `total_amount`

Convert each row to a dictionary and send it to the `green-trips` topic.
You'll need to handle the datetime columns - convert them to strings
before serializing to JSON.

Measure the time it takes to send the entire dataset and flush:

```python
from time import time

t0 = time()

# send all rows ...

producer.flush()

t1 = time()
print(f'took {(t1 - t0):.2f} seconds')
```

How long did it take to send the data?

- 10 seconds 👈 
- 60 seconds
- 120 seconds
- 300 seconds

The result is closer to 17 seconds after removing the time.sleep(0.01) used in the workshop.

~~~bash
...
Sent: GreenTaxiRide(lpep_pickup_datetime='2025-10-31 23:45:00', lpep_dropoff_datetime='2025-11-01 00:08:00', PULocationID=255, DOLocationID=25, passenger_count=0, trip_distance=4.2, tip_amount=4.86, total_amount=37.29)
Sent: GreenTaxiRide(lpep_pickup_datetime='2025-10-31 23:23:00', lpep_dropoff_datetime='2025-10-31 23:37:00', PULocationID=195, DOLocationID=33, passenger_count=0, trip_distance=3.0, tip_amount=0.0, total_amount=19.6)
Data exchange took 17.22 seconds
~~~

## Question 3. Consumer - trip distance

Write a Kafka consumer that reads all messages from the `green-trips` topic
(set `auto_offset_reset='earliest'`).

Count how many trips have a `trip_distance` greater than 5.0 kilometers.

How many trips have `trip_distance` > 5?

- 6506
- 7506
- 8506 👈
- 9506

It is possible to write this directly into the consumer setup but first we didn't go through it in the workshop and when researching on it I thought it was just too complicated. Instead I created a new table in postgres (via pgadmin4) where I sent all the green rides and then query the table. So using: psycopg2, and 

~~~python
for message in consumer:
    ride = message.value
    cur.execute(
        """INSERT INTO green_taxis
           (lpep_pickup_datetime, lpep_dropoff_datetime, PULocationID, DOLocationID, passenger_count, trip_distance, tip_amount, total_amount)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (ride.lpep_pickup_datetime, ride.lpep_dropoff_datetime, ride.PULocationID, ride.DOLocationID,
         ride.passenger_count, ride.trip_distance, ride.tip_amount, ride.total_amount)
~~~

and then

~~~sql
--trip distance > 5 km
select count (*)
from green_taxis
where trip_distance > 5;
~~~


## Part 2: PyFlink (Questions 4-6)

For the PyFlink questions, you'll adapt the workshop code to work with
the green taxi data. The key differences from the workshop:

- Topic name: `green-trips` (instead of `rides`)
- Datetime columns use `lpep_` prefix (instead of `tpep_`)
- You'll need to handle timestamps as strings (not epoch milliseconds)

You can convert string timestamps to Flink timestamps in your source DDL:

```sql
lpep_pickup_datetime VARCHAR,
event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
```

Before running the Flink jobs, create the necessary PostgreSQL tables
for your results.

Important notes for the Flink jobs:

- Place your job files in `workshop/src/job/` - this directory is
  mounted into the Flink containers at `/opt/src/job/`
- Submit jobs with:
  `docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/your_job.py`
- The `green-trips` topic has 1 partition, so set parallelism to 1
  in your Flink jobs (`env.set_parallelism(1)`). With higher parallelism,
  idle consumer subtasks prevent the watermark from advancing.
- Flink streaming jobs run continuously. Let the job run for a minute
  or two until results appear in PostgreSQL, then query the results.
  You can cancel the job from the Flink UI at http://localhost:8081
- If you sent data to the topic multiple times, delete and recreate
  the topic to avoid duplicates:
  `docker exec -it w7_streaming-redpanda-1 rpk topic delete g_rides`


## Question 4. Tumbling window - pickup location

Create a Flink job that reads from `green-trips` and uses a 5-minute
tumbling window to count trips per `PULocationID`.

Write the results to a PostgreSQL table with columns:
`window_start`, `PULocationID`, `num_trips`.

After the job processes all data, query the results:

```sql
SELECT PULocationID, num_trips
FROM <your_table>
ORDER BY num_trips DESC
LIMIT 3;
```

Which `PULocationID` had the most trips in a single 5-minute window?

- 42
- 74
- 75
- 166


## Question 5. Session window - longest streak

Create another Flink job that uses a session window with a 5-minute gap
on `PULocationID`, using `lpep_pickup_datetime` as the event time
with a 5-second watermark tolerance.

A session window groups events that arrive within 5 minutes of each other.
When there's a gap of more than 5 minutes, the window closes.

Write the results to a PostgreSQL table and find the `PULocationID`
with the longest session (most trips in a single session).

How many trips were in the longest session?

- 12
- 31
- 51
- 81


## Question 6. Tumbling window - largest tip

Create a Flink job that uses a 1-hour tumbling window to compute the
total `tip_amount` per hour (across all locations).

Which hour had the highest total tip amount?

- 2025-10-01 18:00:00
- 2025-10-16 18:00:00
- 2025-10-22 08:00:00
- 2025-10-30 16:00:00
