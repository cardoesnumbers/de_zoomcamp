# Module 7 - Streaming

This is the final module of the Data Engineering Zoomcamp and I am taking the chance to try out Zed IDE, let's see how it goes :)

Fast update: As of today (mid May 2026) Zed supports Jupyter kernels through its built-in REPL, notebook-style cells using # %% separators, inline outputs, plots, etc. which is great but i don't want to do that. So... Cursor it is again.


First tip: PS1="> " to remove all the breadcrumbs from the terminal. Add it to the bashcr so it keeps it like that when other terminals are opened. 


Pyarrow we are going to use to read parquet

Docker-compose is work setting up redpanda, the ports are how the producers and consumers will interact with RP

After firing up DP, we create producers and consumers


Once we loaded a sample (1000) of the yellow taxi data we use a row definition to create a class.

Tip: Save all the imports and functions into a single py file, called it models or whatever, then in the jupyter just call on that model like "import from models x or y function" and this keeps the notebook cleaner.


## Creating the producer

- notebook file
- id the parts of the event 
- create a class based on the anatomy of the event
- convert the event to a dictionary
- convert the dictionary to a json string
- define KafkaProducer


| Aspect | Serializer | Deserializer |
| --- | --- | --- |
| Purpose | Python object → Bytes/String | Bytes/String → Python object |
| Used When | Sending data (e.g., Kafka producer) | Receiving data (e.g., Kafka consumer) |
| Example | json.dumps(obj).encode('utf-8') | Ride(**json.loads(data.decode('utf-8'))) |
| Kafka Role | value_serializer in KafkaProducer | value_deserializer in KafkaConsumer |



In this exercise we are using postgres, I am curious to know if duckdb would work as well. But for the sake of the exercise I will keep postgres. One small change is that I dont like too much to write sql queries in the command line so I added a pgadmin service to the docker compose file instead.

After starting the postgres service we need to create a table to receive the data we are sending (rides). Once created we need to make some adjustments in the consumer, the producer remains as it is. To keep things clean I made a copy of the consumer (consumer_db) which needs all the cells to be re-run from start. Once the setup is done I need to resend the events from the producer.

Note: In this exercise we are working with a single consumer but it is possible (probably common) to have multiple consumers moving data to different locations, we would need different group-id.

On Flink, it is presented as a platform that would allow us to preprocess some of the data before it is moved to x or y location and deals with eventuals breaks in connection. Flink is usually built in clusters that are always listening to Kafka streams. Flink takes care of the consumption part and again the producer remains as it is. To work with Flink we need to add it to the docker compose in two parts: a job manager and a task manager (what is actually doing the process)

- Install psycopg2-binary

