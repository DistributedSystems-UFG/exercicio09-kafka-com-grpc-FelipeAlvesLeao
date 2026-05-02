import time
import random
import json
from kafka import KafkaProducer
from const import *

# Connect to the remote Kafka Broker
producer = KafkaProducer(
    bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(2, 8, 0) # Prevents the handshake bug we saw earlier
)

print("Sensor (Node 1) starting. Simulating earthquakes...")

locations = ["Tokyo, Japan", "Los Angeles, CA", "Santiago, Chile", "Jakarta, Indonesia", "Anchorage, AK"]

while True:
    # Simulate a random earthquake
    magnitude = round(random.uniform(1.0, 9.0), 1)
    location = random.choice(locations)
    
    earthquake = {
        "magnitude": magnitude,
        "location": location
    }
    