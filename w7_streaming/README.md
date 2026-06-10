# Module 7 - Streaming

## Module comments and observations

This is the final module of the Data Engineering Zoomcamp.

Ingredients for this module:
- Docker for Flink + adapters, Postgres/PgAdmin, Redpanda
- Python, psycopg2
- NYC Taxi Data
- Cursor 


### Concepts to keep in mind
- Data streaming: exchanging of data in "real time".
- Kafka cluster: nodes/machines talking to each other in a network.
- Producer: the one posting the information, it talks in terms of events or messages.
- Consumer: the one subscribed to the information being posted.
- Topic: A continous stream of events defined by user, key-values. A topic is stored in one node of a Kafka cluster.
- Event/Msg: a data point at a certain timestamp, a collection of events go into a topic which in turn are read by the (subscribed) consumers. Each event contains a message.
- Message: whats inside of the event, has three structures: key, value, timestamp.
- Replication (factor): duplication a topic in +1 node. A leader node is defined here as well +1 node follower. Producers and consumers talk to the node leader. If node leader dies, the cluster adjusts and moves to node follower without much interruption in the work producer and consumer are doing. Follower becomes a leader and any other free nodes become follower, and so on.
- Logs: How we store events in a topic

The work at hand is to produce simulated real-live events using a producer, use Redpanda to simplify what Kafka would have done when making the data available to a consumer. Eventually moving the data to a database (Postgres). 

### Why Redpanda?
- Reliability and robustness to the topic (replication).
- Flexibility when it comes to the size/extent of the topics
- Scalability

We worked with serializers and deserializers to convert data in a format that is compatible with streaming. 

To avoid having to call up (de)serializers on multiple cells, definitions for each one have been save on an py file named models which I will use in the exercise to call for all the needed imports and above-mentioned functions. Like this:

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

**Quick summary on when to use each one:**

| Aspect | Serializer | Deserializer |
| --- | --- | --- |
| Purpose | Python object → Bytes/String | Bytes/String → Python object |
| Used When | Sending data (e.g., Kafka producer) | Receiving data (e.g., Kafka consumer) |
| Example | json.dumps(obj).encode('utf-8') | Ride(**json.loads(data.decode('utf-8'))) |
| Kafka Role | value_serializer in KafkaProducer | value_deserializer in KafkaConsumer |


Kafka/Redpanda and Postgres speak different language, one bytes/json and the other pure SQL so psycopg2 works as receiver and interpreter via a python script.

In this exercise I am using postgres, I am curious to know if duckdb would work as Ill. But for the sake of the exercise I will keep postgres. One small change is that I dont like to write sql queries in the command line so I added a pgadmin service to the docker compose file instead.

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

After starting the postgres service I need to create a table to receive the data I am sending (rides). This table should have the same structure as my rides, in other words, this:

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


Once created I need to make some adjustments in the consumer (new file), the producer remains as it is. Once the setup is done I need to resend the events from the producer.

Note: In this exercise I am working with a single consumer but it is possible (probably common) to have multiple consumers moving data to different locations, I would need different group-id.

On to Flink. Flink is presented as a platform that would allow us to preprocess some of the data before it is moved to x or y location, Flink is also capable of dealing with common challenges like eventual breaks in connection. Flink is usually built in clusters that are always listening to the streams. Flink takes care of the consumption part and again the producer remains as it is. To work with Flink I need to add it to the docker compose in two parts: 

- a job manager (deciding to which task manager each job goes) and, 
- a task manager (what is actually doing the processes). 

The actual setup for flink is done via a flink-config (some config), a pyprojectflink.toml (dependencies), and a dockerfile where everything comes together.

After adding them to the docker compose I execute both of them. 

~~~bash
docker compose up jobmanager taskmanager
~~~

Reminder: Before trying to configure any type of aggregation in Flink I need to cancel any ongoing job. For the aggregation I create a new table in pgadmin. 


### Additional notes
- Check on Confluent cloud, video is 3 years old, is it still relevant?
