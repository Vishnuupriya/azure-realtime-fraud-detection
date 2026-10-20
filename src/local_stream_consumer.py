
import json
import time
from collections import Counter

from transaction_simulator import generate_transaction


def main():
    print("Local banking stream started.")
    print("Press Ctrl+C to stop.\n")

    scenario_counts = Counter()
    total_transactions = 0
    total_fraud = 0

    try:
        while True:
            transaction = generate_transaction()

            # Simulate an event arriving from a streaming source.
            event_json = json.dumps(transaction)

            # Simulate the consumer parsing the incoming event.
            event = json.loads(event_json)

            total_transactions += 1
            scenario_counts[event["transaction_type"]] += 1

            if event["is_fraud"]:
                total_fraud += 1

            print(
                f"Event #{total_transactions} | "
                f"ID: {event['transaction_id'][:8]} | "
                f"Amount: ₹{event['amount']:.2f} | "
                f"Scenario: {event['transaction_type']} | "
                f"Fraud label: {event['is_fraud']}"
            )

            if total_transactions % 10 == 0:
                print("\n--- Streaming Summary ---")
                print("Total events:", total_transactions)
                print("Scenario counts:", dict(scenario_counts))
                print("Fraud-labelled events:", total_fraud)
                print("-------------------------\n")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nLocal stream stopped.")
        print("Total events processed:", total_transactions)


if __name__ == "__main__":
    main()
