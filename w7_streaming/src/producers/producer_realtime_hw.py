import dataclasses
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

scripts_dir = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from kafka import KafkaProducer
from models import TaxiRide

def ride_serializer(ride):
    return json.dumps(dataclasses.asdict(ride)).encode('utf-8')


server = 'localhost:9092'
producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=ride_serializer,
)

topic_name = 'rides'
count = 0

print("Sending events (Ctrl+C to stop)...")
print()

try:
    while True:
        # ~20% chance of a late event (3-10 seconds old)
        if random.random() < 0.2:
            delay = random.randint(3, 10)
            ride = make_ride(delay_seconds=delay)
            ts = datetime.fromtimestamp(ride.tpep_pickup_datetime / 1000, tz=timezone.utc)
            print(f"  LATE ({delay}s) -> PU={ride.PULocationID} ts={ts:%H:%M:%S}")
        else:
            ride = make_ride()
            ts = datetime.fromtimestamp(ride.tpep_pickup_datetime / 1000, tz=timezone.utc)
            print(f"  on time   -> PU={ride.PULocationID} ts={ts:%H:%M:%S}")

        producer.send(topic_name, value=ride)
        count += 1
        time.sleep(0.5)

except KeyboardInterrupt:
    producer.flush()
    print(f"\nSent {count} events")