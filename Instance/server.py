import grpc
from concurrent import futures
import threading
import json
from kafka import KafkaConsumer
from const import *

import earthquake_pb2
import earthquake_pb2_grpc

# A simple dictionary acting as our "database"
latest_earthquake = {"magnitude": 0.0, "location": "None"}

# --- JOB 1: KAFKA CONSUMER (Runs in the background) ---
def consume_kafka():
    global latest_earthquake
    consumer = KafkaConsumer(
        'processed_earthquakes',
        bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        api_version=(2, 8, 0)
    )
    print("Server is listening to Kafka for processed earthquakes...")
    
    for msg in consumer:
        latest_earthquake = msg.value
        print(f"[STORED] Database updated with: {latest_earthquake}")