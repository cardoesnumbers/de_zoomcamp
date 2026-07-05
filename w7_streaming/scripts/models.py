import json
import dataclasses

from dataclasses import dataclass


@dataclass #yellow taxi 
class TaxiRide:
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    total_amount: float
    tpep_pickup_datetime: int  # epoch milliseconds

def ride_from_row(row):
    return TaxiRide(
        PULocationID=int(row['PULocationID']),
        DOLocationID=int(row['DOLocationID']),
        trip_distance=float(row['trip_distance']),
        total_amount=float(row['total_amount']),
        tpep_pickup_datetime=int(row['tpep_pickup_datetime'].timestamp() * 1000),
    )

@dataclass #homework 
class GreenTaxiRide:
    lpep_pickup_datetime: str
    lpep_dropoff_datetime: str
    PULocationID: int
    DOLocationID: int
    passenger_count: int
    trip_distance: float
    tip_amount: float
    total_amount: float
    
def green_ride_from_row(row):
    return GreenTaxiRide(
        lpep_pickup_datetime=str(row['lpep_pickup_datetime']),
        lpep_dropoff_datetime=str(row['lpep_dropoff_datetime']),
        PULocationID=int(row['PULocationID']),
        DOLocationID=int(row['DOLocationID']),
        passenger_count=int(row['passenger_count']),
        trip_distance=float(row['trip_distance']),
        tip_amount=float(row['tip_amount']),
        total_amount=float(row['total_amount']),
    )

def ride_serializer(ride): 
    ride_dict = dataclasses.asdict(ride)
    ride_json = json.dumps(ride_dict).encode('utf-8')
    return ride_json

# The serializer converts the class to a dictionary using dataclasses.asdict 
# Then converts the python object (dict) to a JSON string (using json.dumps()).
# Finally, it encodes the JSON string as bytes (using .encode('utf-8')).
# The serializer can be used for both the workshop and the homework, as it works for both TaxiRide and GreenTaxiRide classes.



def ride_deserializer(data):
    json_str = data.decode('utf-8')
    ride_dict = json.loads(json_str)
    return TaxiRide(**ride_dict)

def green_ride_deserializer(data):
    json_str = data.decode('utf-8')
    ride_dict = json.loads(json_str)
    return GreenTaxiRide(**ride_dict)


# A deserializer converts raw data (bytes/strings) → Python objects.
# In Kafka, deserializers are used in consumers to reconstruct objects from bytes.


