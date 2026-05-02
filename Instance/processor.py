from kafka import KafkaConsumer, KafkaProducer
import json
from const import *

# Connect the consumer to listen for raw data
consumer = KafkaConsumer(
    'raw_earthquakes', 
    bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Connect the producer to send processed data
producer = KafkaProducer(
    bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Node 2 (Processor) is listening for raw earthquakes...")

for msg in consumer:
    earthquake = msg.value
    
    # The Processing Logic: Filter for magnitude >= 5.0
    if earthquake.get('magnitude', 0) >= 5.0:
        print(f"[PROCESSED] Significant earthquake! Forwarding: {earthquake}")
        producer.send('processed_earthquakes', value=earthquake)
        producer.flush()