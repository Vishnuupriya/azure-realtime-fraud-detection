
import json
import random
import time
import uuid
from datetime import datetime, timezone


MERCHANTS = [
    "Grocery Store",
    "Electronics Store",
    "Fuel Station",
    "Online Shopping",
    "Restaurant",
]

LOCATIONS = [
    "Chennai",
    "Bengaluru",
    "Mumbai",
    "Hyderabad",
    "Delhi",
]


def generate_transaction():
    """Generate one synthetic banking transaction."""

    scenario = random.choices(
        ["NORMAL", "HIGH_VALUE", "UNUSUAL_LOCATION"],
        weights=[90, 5, 5],
        k=1,
    )[0]

    if scenario == "NORMAL":
        amount = round(random.uniform(100, 10000), 2)
        location = "Chennai"
        is_fraud = False

    elif scenario == "HIGH_VALUE":
        amount = round(random.uniform(50000, 150000), 2)
        location = "Chennai"
        is_fraud = True

    else:
        amount = round(random.uniform(100, 10000), 2)
        location = random.choice(
            [city for city in LOCATIONS if city != "Chennai"]
        )
        is_fraud = True

    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "account_id": f"ACC{random.randint(1000, 1020)}",
        "amount": amount,
        "merchant": random.choice(MERCHANTS),
        "location": location,
        "transaction_timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": f"DEV{random.randint(100, 120)}",
        "is_fraud": is_fraud,
        "transaction_type": scenario,
    }

    return transaction


def main():
    """Continuously generate transactions."""

    print("Banking transaction simulator started.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            transaction = generate_transaction()
            print(json.dumps(transaction))
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nSimulator stopped.")


if __name__ == "__main__":
    main()
