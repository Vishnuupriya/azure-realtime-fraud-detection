
from collections import Counter
from transaction_simulator import generate_transaction


def main():
    transactions = [generate_transaction() for _ in range(1000)]

    scenario_counts = Counter(
        transaction["transaction_type"]
        for transaction in transactions
    )

    fraud_count = sum(
        transaction["is_fraud"]
        for transaction in transactions
    )

    transaction_ids = [
        transaction["transaction_id"]
        for transaction in transactions
    ]

    print("Total transactions:", len(transactions))
    print("Unique transaction IDs:", len(set(transaction_ids)))
    print("Scenario distribution:", dict(scenario_counts))
    print("Fraud-labelled transactions:", fraud_count)

    assert len(transactions) == 1000
    assert len(set(transaction_ids)) == 1000
    assert all(transaction["amount"] > 0 for transaction in transactions)
    assert all(
        transaction["transaction_type"]
        in {"NORMAL", "HIGH_VALUE", "UNUSUAL_LOCATION"}
        for transaction in transactions
    )

    print("Validation successful!")


if __name__ == "__main__":
    main()
