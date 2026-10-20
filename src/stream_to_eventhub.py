
import json
import os
import time

from dotenv import load_dotenv
from azure.eventhub import EventData, EventHubProducerClient

from transaction_simulator import generate_transaction

load_dotenv()

connection_string = os.getenv("EVENT_HUBS_CONNECTION_STRING")
event_hub_name = os.getenv("EVENT_HUB_NAME")

if not connection_string or not event_hub_name:
    raise ValueError("Event Hubs configuration is missing.")

producer = EventHubProducerClient.from_connection_string(
    conn_str=connection_string,
    eventhub_name=event_hub_name,
)

print("Streaming transactions to Azure Event Hubs.")
print("Press Ctrl+C to stop.")

try:
    while True:
        transaction = generate_transaction()

        batch = producer.create_batch()
        batch.add(EventData(json.dumps(transaction)))
        producer.send_batch(batch)

        print(
            f"Sent {transaction['transaction_id'][:8]} | "
            f"₹{transaction['amount']:.2f} | "
            f"{transaction['transaction_type']}"
        )

        time.sleep(2)

except KeyboardInterrupt:
    print("\nStreaming stopped.")

finally:
    producer.close()
