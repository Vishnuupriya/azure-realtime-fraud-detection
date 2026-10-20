# Real-Time Banking Transaction Fraud Detection

## Project Overview

An end-to-end Azure Data Engineering project that simulates banking transactions, streams events for processing, and identifies suspicious transaction patterns.

## Business Problem

Banks need to process transactions in near real time to identify potentially fraudulent activity and make transaction monitoring more effective.

## Planned Architecture

Python Transaction Simulator → Azure Event Hubs → Azure Databricks Structured Streaming → Delta Lake (Bronze, Silver, Gold) → Power BI

## Technology Stack

- Python
- Azure Event Hubs
- Azure Databricks
- PySpark and Structured Streaming
- Delta Lake
- Power BI
- Git and GitHub

## Current Progress

- [x] Local project structure created
- [x] Transaction data dictionary documented
- [x] Synthetic transaction simulator implemented
- [x] Unit tests created
- [x] Transaction validation script implemented
- [ ] Azure Event Hubs integration
- [ ] Databricks streaming pipeline
- [ ] Bronze, Silver, and Gold Delta tables
- [ ] Fraud monitoring dashboard

## Run Locally

Start the transaction simulator:

`python src/transaction_simulator.py`

Validate 1,000 generated transactions:

`python src/validate_transactions.py`

Run unit tests:

`python -m unittest discover -s tests -v`

## Data Disclaimer

All transactions are synthetic and intended for learning and demonstration. The simulated fraud labels are not a production fraud-detection model.