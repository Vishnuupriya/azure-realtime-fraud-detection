
import json
import os

from azure.eventhub import EventData, EventHubProducerClient
from dotenv import load_dotenv

load_dotenv()


def publish_transaction(transaction):
    """Publish one transaction to Azure Event Hubs."""

    connection_string = os.getenv("EVENT_HUBS_CONNECTION_STRING")
    event_hub_name = os.getenv("EVENT_HUB_NAME")

    if not connection_string or not event_hub_name:
        raise ValueError(
            "Configure EVENT_HUBS_CONNECTION_STRING and "
            "EVENT_HUB_NAME before publishing."
        )

    producer = EventHubProducerClient.from_connection_string(
        conn_str=connection_string,
        eventhub_name=event_hub_name,
    )

    try:
        batch = producer.create_batch()
        batch.add(EventData(json.dumps(transaction)))
        producer.send_batch(batch)
    finally:
        producer.close()
