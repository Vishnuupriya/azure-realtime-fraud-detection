# Real-Time Banking Transaction Fraud Detection

An end-to-end Azure Data Engineering project that ingests simulated banking transactions in real time, processes them using Azure Databricks and PySpark, stores data in a Bronze–Silver–Gold Lakehouse architecture, and presents fraud analytics through Power BI.

## Project Overview

Financial institutions need to process transactions continuously, maintain reliable data quality, and identify potentially suspicious activities. This project demonstrates a real-time data pipeline using Azure services to ingest, transform, validate, and analyze banking transactions.

The pipeline uses a Python transaction simulator to generate events, Azure Event Hubs to ingest streaming data, Azure Databricks Structured Streaming to process events, Azure Data Lake Storage Gen2 to store Delta Lake data, and Power BI to visualize aggregated results.

**Project type:** Real-time data engineering and fraud analytics  
**Domain:** Banking and financial services  
**Processing:** Streaming ingestion and data transformation  
**Architecture:** Medallion Lakehouse (Bronze, Silver, Gold)

## Architecture

```text
Python Transaction Simulator
            |
            v
    Azure Event Hubs
            |
            v
 Azure Databricks
 PySpark Structured Streaming
            |
            v
   Bronze Delta Lake
   Raw transaction events
            |
            v
   Silver Delta Lake
 Parsing, validation,
 cleaning and deduplication
            |
            v
    Gold Delta Lake
 Transaction aggregations
 and fraud analytics
            |
       +----+-----+
       |          |
       v          v
 Power BI     Data Quality
 Dashboard    & Fraud Alerts
```

The Power BI dashboard uses an exported CSV snapshot of the Gold analytics data. It is not configured as an automatically refreshing live connection.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Simulates banking transactions and sends events |
| Azure Event Hubs | Streaming event ingestion |
| Azure Databricks | Distributed data processing |
| PySpark Structured Streaming | Processes continuous transaction streams |
| Azure Data Lake Storage Gen2 | Stores Bronze, Silver and Gold data |
| Delta Lake | Provides reliable table storage and transactional data management |
| Databricks Unity Catalog | Manages storage credentials and external locations |
| Power BI Service | Visualizes transaction and fraud analytics |
| Git and GitHub | Source control and project documentation |
| VS Code | Local development |

## Key Features

- Real-time transaction event generation using Python.
- Streaming ingestion through Azure Event Hubs.
- Kafka-compatible Event Hubs integration with Databricks.
- Bronze, Silver and Gold Lakehouse layers.
- JSON parsing and schema-based data extraction.
- Data validation, null filtering and duplicate transaction handling.
- Merchant- and transaction-type-level aggregations.
- Fraud counts and fraud-rate calculations.
- Data quality checks for missing identifiers, invalid amounts and timestamps.
- Rule-based fraud alert candidates using simulator-provided fraud flags and transaction types.
- Power BI visualizations for transaction volume, amounts and fraud analytics.
- Git-based project version control.

## Data Flow and Implementation

### 1. Generate banking transactions

A Python transaction simulator generates sample banking events containing transaction details such as:

- `transaction_id`
- `account_id`
- `transaction_timestamp`
- `amount`
- `merchant`
- `location`
- `device_id`
- `transaction_type`
- `is_fraud`

The simulator is intended for development and demonstration, using synthetic data rather than real customer transactions.

### 2. Ingest events using Azure Event Hubs

The Python producer sends transaction events to the `banking-transactions` Event Hub.

Azure Event Hubs acts as the streaming ingestion layer between the transaction producer and Databricks.

### 3. Process the stream using Azure Databricks

Databricks consumes events through its Kafka-compatible interface using PySpark Structured Streaming.

The ingestion process captures the raw event payload along with metadata such as topic, partition, offset, Kafka timestamp and ingestion timestamp.

### 4. Bronze layer — raw data

The Bronze layer stores the incoming transaction payloads in Delta format.

**Purpose:**
- Preserve the ingested event payload.
- Retain source metadata for traceability.
- Provide a foundation for downstream transformations.

**Storage location:** `bronze/banking_transactions/`

### 5. Silver layer — cleaned transactions

The Silver layer parses the JSON payload into structured columns and applies validation rules.

**Transformations include:**
- Extracting transaction fields from JSON.
- Converting transaction timestamps into timestamp values.
- Filtering records with missing required identifiers.
- Excluding null, zero or negative transaction amounts.
- Excluding records with invalid or missing timestamps.
- Applying watermarking and transaction-ID deduplication.

The resulting data is stored as a Delta table for downstream analytics.

**Storage location:** `silver/banking_transactions/`

### 6. Gold layer — fraud analytics

The Gold layer aggregates Silver transactions by merchant and transaction type.

The output includes:

| Column | Description |
|---|---|
| `merchant` | Merchant associated with the transactions |
| `transaction_type` | Type or category of transaction |
| `total_transactions` | Number of transactions in the group |
| `total_amount` | Sum of transaction amounts |
| `fraud_count` | Number of transactions marked as fraudulent |
| `fraud_rate_pct` | Percentage of transactions marked as fraudulent |

The fraud rate is calculated as:

`fraud_rate_pct = (fraud_count / total_transactions) × 100`

These aggregations provide a summary of transaction activity and simulator-labeled fraud patterns.

**Storage location:** `gold/fraud_analytics/`

### 7. Data quality checks and fraud alerts

The data quality notebook checks the Silver dataset for:

- Total record count.
- Missing transaction IDs.
- Missing account IDs.
- Invalid transaction amounts.
- Missing or invalid timestamps.

A separate alert-candidate dataset identifies transactions based on the simulator's `is_fraud` flag and selected transaction types, such as `HIGH_VALUE` and `UNUSUAL_LOCATION`.

These checks and alert candidates are currently notebook-based processing steps. They do not represent a fully automated alert delivery or incident-management system.

### 8. Power BI dashboard

The Gold aggregation data is exported to CSV for use in Power BI Service.

The dashboard includes:

- **Total Transactions:** total transaction count.
- **Fraud Count:** number of transactions flagged as fraudulent.
- **Total Transaction Amount:** sum of transaction amounts.
- **Fraud by Merchant:** comparison of fraud counts across merchants.
- **Transaction Amount by Merchant:** comparison of transaction amounts.
- **Transaction Summary:** table of merchant and transaction-type analytics.

The current implementation uses a CSV snapshot. To display newer results, export the latest Gold data and refresh or replace the imported data in Power BI.

## Project Structure

```text
azure-realtime-fraud-detection/
├── docs/
│   └── screenshots/
├── src/
│   ├── transaction_simulator.py
│   ├── eventhub_producer.py
│   ├── stream_to_eventhub.py
│   ├── local_stream_consumer.py
│   └── test_eventhub_connection.py
├── tests/
├── notebooks/
│   ├── 01_eventhub_stream_ingestion
│   ├── 02_silver_transformation
│   ├── 03_gold_fraud_analytics
│   └── 04_data_quality_and_fraud_alerts
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: The notebook filenames above describe the intended organization. Export the actual Databricks notebooks into `notebooks/` and adjust this tree to match the files committed to GitHub.*

## Prerequisites

Before running the project, prepare:

- A Python environment and VS Code.
- An Azure subscription with permission to create the required resources.
- An Azure Event Hubs namespace and event hub.
- An Azure Databricks workspace with suitable compute.
- An Azure Data Lake Storage Gen2 account with hierarchical namespace enabled.
- Storage credentials and permissions configured for Databricks access.
- Power BI Service for dashboard creation.

Azure services may incur charges. Review resource pricing, monitor usage and stop or remove resources when they are no longer needed.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/azure-realtime-banking-fraud-detection.git
cd azure-realtime-banking-fraud-detection
```

Replace `YOUR-USERNAME` with your GitHub username and use the actual URL of your repository.

### 2. Create a Python virtual environment

On Windows Command Prompt:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in the values required by the producer scripts.

For example, the configuration may contain:

```dotenv
EVENTHUB_CONNECTION_STRING=YOUR_EVENT_HUB_CONNECTION_STRING
EVENTHUB_NAME=banking-transactions
```

Use the variable names expected by the actual Python scripts. The example above is illustrative; update it to match the implementation.

**Security:** Never commit `.env`, connection strings, access keys, passwords or other secrets to GitHub. Keep only placeholder values in `.env.example`.

### 5. Run the transaction producer

Run the script that sends transactions to Event Hubs:

```bat
python src/stream_to_eventhub.py
```

If your implementation uses `eventhub_producer.py` as the main entry point, run that script instead. Keep the producer running while testing ingestion.

## Databricks Execution Order

Run the notebooks in the following sequence:

1. `01_eventhub_stream_ingestion` — read events from Event Hubs and write raw events to Bronze Delta Lake.
2. `02_silver_transformation` — parse, validate and deduplicate the Bronze records.
3. `03_gold_fraud_analytics` — aggregate transaction data for fraud analytics.
4. `04_data_quality_and_fraud_alerts` — run quality checks and generate a fraud alert-candidate snapshot.

Configure each notebook with the appropriate storage paths, secret scope and Event Hubs settings for your Azure environment.

Streaming notebooks require explicit checkpoint locations to track processing progress. Avoid deleting existing checkpoints casually: they are needed for recovery, and resetting them may cause records to be replayed or skipped depending on the source offsets and retention.

## Screenshots

Store actual screenshots from your environment under `docs/screenshots/`.

Recommended screenshots:

1. `01-event-hubs.png` — Event Hubs namespace and event hub.
2. `02-bronze-ingestion.png` — successful Databricks streaming ingestion.
3. `03-silver-transactions.png` — cleaned Silver transaction records.
3. `03a-silver-transactions.png` — silver_query graph
4. `04-gold-fraud-analytics.png` — Gold aggregation results.
5. `05-power-bi-dashboard.png` — completed Power BI dashboard.
6. `06-data-quality-alerts.png` — data quality results and alert candidates, if implemented.
6. `06-fraud-alerts.png` — fraud alert.
7. `07-resource-group.png` — folder that contains all azure resources.

Embed the screenshots in this README using relative paths. For example:

```markdown
![Power BI Fraud Analytics Dashboard](docs/screenshots/05-power-bi-dashboard.png)
```

Only include screenshots that actually exist in the repository. Hide sensitive identifiers and credentials before uploading them.

## Security and Reliability Considerations

- Use Databricks secrets for sensitive connection details.
- Apply least-privilege permissions to Event Hubs and storage.
- Keep credentials out of source code and version control.
- Use separate checkpoint locations for independent streaming queries.
- Monitor streaming query status and exceptions instead of relying only on a successful `.start()` call.
- Handle source retention and checkpoint recovery carefully to avoid data loss.
- Validate transaction data before downstream analytics.
- Use synthetic data for public demonstrations.

## Current Scope and Limitations

- The project demonstrates a streaming data engineering pipeline, not a production banking platform.
- Fraud labels originate from the simulator; no trained machine-learning model currently predicts fraud.
- Fraud-rate calculations reflect the available sample data and its labels.
- Fraud alert candidates are generated in a notebook; automatic notifications are not currently configured.
- Power BI consumes an exported CSV snapshot rather than a live streaming connection.
- Production-grade monitoring, alert delivery, access auditing and automated deployment can be added as future enhancements.

## Future Enhancements

- Implement machine-learning-based fraud prediction.
- Add automated alerts through Azure Functions, Logic Apps or another notification service.
- Automate Gold data export and Power BI refresh.
- Orchestrate batch workflows and recovery with Azure Data Factory or Databricks Jobs.
- Add automated unit and data quality tests.
- Implement CI/CD and environment-specific deployment.
- Add monitoring, logging, error handling and operational dashboards.

## Learning Outcomes

This project demonstrates practical experience with:

- Building an end-to-end Azure data pipeline.
- Streaming ingestion using Azure Event Hubs.
- PySpark Structured Streaming and Kafka-compatible sources.
- Lakehouse architecture using Bronze, Silver and Gold layers.
- Delta Lake storage and streaming checkpoints.
- Data validation, deduplication and aggregation.
- Fraud analytics and Power BI reporting.
- Python development, Git and GitHub project documentation.

## Author

**Azure Data Engineering Portfolio Project**

Technologies: Azure Event Hubs | Azure Databricks | PySpark | Delta Lake | ADLS Gen2 | Power BI

---

*This project was developed for learning and portfolio demonstration using simulated banking transaction data.*
