
import sys
import unittest
from pathlib import Path

# Make the src directory importable
sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "src")
)

from transaction_simulator import generate_transaction


class TestTransactionSimulator(unittest.TestCase):

    def test_transaction_has_required_fields(self):
        transaction = generate_transaction()

        expected_fields = {
            "transaction_id",
            "account_id",
            "amount",
            "merchant",
            "location",
            "transaction_timestamp",
            "device_id",
            "is_fraud",
            "transaction_type",
        }

        self.assertEqual(set(transaction.keys()), expected_fields)

    def test_transaction_id_is_unique(self):
        transactions = [generate_transaction() for _ in range(100)]
        transaction_ids = [
            transaction["transaction_id"]
            for transaction in transactions
        ]

        self.assertEqual(len(transaction_ids), len(set(transaction_ids)))

    def test_transaction_data_types(self):
        transaction = generate_transaction()

        self.assertIsInstance(transaction["transaction_id"], str)
        self.assertIsInstance(transaction["account_id"], str)
        self.assertIsInstance(transaction["amount"], float)
        self.assertIsInstance(transaction["is_fraud"], bool)

    def test_transaction_amount_is_positive(self):
        for _ in range(100):
            transaction = generate_transaction()
            self.assertGreater(transaction["amount"], 0)

    def test_transaction_type_is_valid(self):
        transaction = generate_transaction()

        self.assertIn(
            transaction["transaction_type"],
            ["NORMAL", "HIGH_VALUE", "UNUSUAL_LOCATION"],
        )


if __name__ == "__main__":
    unittest.main()
