# Module 7 - Streaming

## Module comments and observations

This is the final module of the Data Engineering Zoomcamp and I am taking the chance to try out Zed IDE, let's see how it goes :)

Fast update: As of today (mid May 2026) Zed supports Jupyter kernels through its built-in REPL, notebook-style cells using # %% separators, inline outputs, plots, etc. which is great but i don't want to do that. So... Cursor it is again.

In this module I are going to be using Pyarrow to read parquet files.Docker-compose will be used to setting up redpanda, the ports defined in the yaml are how the producers and consumers will interact with each other.

After firing up DP, I create producers and consumers


Once I loaded a sample (1000) of the yellow taxi data I use a row definition to create a class.

Tip: To avoid having to call up (de)serializers on multiple cells, definitions for each one have been save on an py file named models which I will use in the exercise to call for all the needed imports and above-mentioned functions. 

Why Kafka?
Reliability and robustness to the topic (replication).
Flexibility when it comes to the size/extent of the topics
Scalability

Concepts to keep in mind:
- Data streaming: exchanging of data in "real time"
- Producer: the one posting the information
- Consumer: the one subscribed to the information being posted
- Topic: A continous stream of events
- Event: a data point at a certain timestamp, a collection of events go into a topic which in turn are read by the (subscribed) consumers. Each event contains a message.
- Message: whats inside of the event, has three structures: key, value, timestamp.
- Logs: How we store events in a topic


## Creating the producer

- (notebook file)
- identify the parts of the event 
- create a class based on the anatomy of the event
- convert the event to a dictionary*
- convert the dictionary to a json string*
- define KafkaProducer including servers and topic name

* these steps are automated with a **serializer**

## Creating the consumer (local/db)
- (separate notebook but im guessing this doesn't mattered much)
- define the consumer including server and topic name are the same as in the producer and the value **deserializer**. In Kafka, deserializers are used in consumers to reconstruct objects from bytes (created by the serializer)

**Quick summary on when to use each one:**

| Aspect | Serializer | Deserializer |
| --- | --- | --- |
| Purpose | Python object → Bytes/String | Bytes/String → Python object |
| Used When | Sending data (e.g., Kafka producer) | Receiving data (e.g., Kafka consumer) |
| Example | json.dumps(obj).encode('utf-8') | Ride(**json.loads(data.decode('utf-8'))) |
| Kafka Role | value_serializer in KafkaProducer | value_deserializer in KafkaConsumer |

- db: psycopg2! 

Kafka and Postgres speak different language, one bytes/json and the other pure SQL so psycopg2 works as receiver and interpreter via a python script.





In this exercise I are using postgres, I am curious to know if duckdb would work as Ill. But for the sake of the exercise I will keep postgres. One small change is that I dont like to write sql queries in the command line so I added a pgadmin service to the docker compose file instead.

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

After starting the postgres service I need to create a table to receive the data I are sending (rides). This table should have the same structure as my rides, in other words, this:

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


Once created I need to make some adjustments in the consumer, the producer remains as it is. To keep things clean I made a copy of the consumer (consumer_db) which requires all the cells to be re-run from start. Once the setup is done I need to resend the events from the producer.

Note: In this exercise I are working with a single consumer but it is possible (probably common) to have multiple consumers moving data to different locations, I would need different group-id.

On Flink, Flink is presented as a platform that would allow us to preprocess some of the data before it is moved to x or y location and deals with eventuals breaks in connection. Flink is usually built in clusters that are always listening to Kafka streams. Flink takes care of the consumption part and again the producer remains as it is. To work with Flink I need to add it to the docker compose in two parts: 

- a job manager (deciding to which task manager each job goes) and, 
- a task manager (what is actually doing the processes). 

The actual setup for flink is done via a flink-config (some config), a pyprojectflink.toml (dependencies), and a dockerfile (where everything comes together.

After having added them to the docker compose I execute both of them. 

~~~bash
docker compose up jobmanager taskmanager
~~~

Before trying to configure any type of aggregation in Flink I need to cancel any ongoing job. For the aggregation I create a new table in pgadmin. 



