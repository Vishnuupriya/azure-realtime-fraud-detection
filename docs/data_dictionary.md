# Banking Transaction Data Dictionary

| Column | Data Type | Description |
|---|---|---|
| transaction_id | String | Unique transaction identifier |
| account_id | String | Synthetic bank account identifier |
| amount | Decimal | Transaction amount in INR |
| merchant | String | Merchant where the payment occurred |
| location | String | Transaction location |
| transaction_timestamp | Timestamp | Time the transaction occurred |
| device_id | String | Device used to initiate the transaction |
|transaction_type| String| Synthetic scenario category assigned to thetransaction|
| is_fraud | Boolean | Synthetic fraud label: true or false |

## Project Assumptions

- All transaction records are synthetic.
- Transaction amounts are denominated in INR.
- Transactions will be generated continuously to simulate real-time banking activity.
- Fraud labels are included for evaluating the detection pipeline.
- The pipeline will later use Azure Event Hubs, Azure Databricks, Delta Lake, and Power BI.