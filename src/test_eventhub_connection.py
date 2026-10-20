
import os
import json
from dotenv import load_dotenv
from azure.eventhub import EventData, EventHubProducerClient

from transaction_simulator import generate_transaction

load_dotenv()

connection_string = os.getenv("EVENT_HUBS_CONNECTION_STRING")
event_hub_name = os.getenv("EVENT_HUB_NAME")

if not connection_string or not event_hub_name:
    raise ValueError("Event Hubs configuration is missing.")

transaction = generate_transaction()

producer = EventHubProducerClient.from_connection_string(
    conn_str=connection_string,
    eventhub_name=event_hub_name,
)

try:
    batch = producer.create_batch()
    batch.add(EventData(json.dumps(transaction)))
    producer.send_batch(batch)

    print("Test transaction sent successfully!")
    print("Transaction ID:", transaction["transaction_id"])
    print("Scenario:", transaction["transaction_type"])
finally:
    producer.close()
