# Customer 360 Data Engineering Demo

This is a small, runnable data engineering portfolio project that shows how raw customer data can be validated, transformed, aggregated, and prepared for machine learning. The project simulates a retail Customer 360 use case where customer identity, orders, website activity, and support tickets are combined into one analytics-ready data product.

The goal is not to build a large production platform. The goal is to demonstrate practical data engineering fundamentals in a project that a reviewer can clone, run, test, and understand quickly.

## Data Source

The data in `data/raw/` is synthetic sample data created by ChatGPT for this portfolio project. It is not copied from a real company, public dataset, customer system, or Kaggle dataset.

The sample data was designed to look like realistic retail source-system extracts:

- `customers.csv`: customer profile and acquisition data
- `orders.csv`: order history with completed and returned orders
- `web_events.csv`: website behavior and checkout events
- `support_tickets.csv`: customer support case history

Because the data is synthetic, the project is safe to publish on GitHub and does not contain personal, confidential, or production information.

## What This Project Does

The pipeline builds a local Customer 360 data product from the synthetic raw datasets. It:

1. Reads CSV source files from `data/raw/`.
2. Validates required schemas and basic data quality rules.
3. Loads the data into a local SQLite warehouse.
4. Runs SQL transformations to aggregate customer-level features.
5. Exports `customer_360.csv` with one row per customer.
6. Trains a simple churn model using the Customer 360 output.
7. Includes Snowflake-style SQL showing how a legacy Hive/Spark dataset could be migrated.

## Problem Set

A retail business has customer, order, web event, and support-ticket data spread across different systems. The analytics team needs a reliable Customer 360 table that can answer:

- Which customers are most valuable?
- Which customers are at risk of churn?
- Which source records are invalid before they enter the data product?
- How would a legacy Hive/Spark table be migrated into a Snowflake model?

## Expected Outcome

The pipeline builds `customer_360` with one row per customer, including revenue, order frequency, web activity, support activity, and churn labels. It also trains a simple churn model locally using the same script shape that can be used as an AWS SageMaker training entrypoint.

Generated outputs:

- `build/customer360.db`: SQLite warehouse with raw, staging, and mart tables
- `build/customer_360.csv`: Customer 360 data product
- `build/model_metrics.json`: churn-model metrics
- `build/churn_model.joblib`: trained scikit-learn model

## Findings From This Demo

After running the pipeline on the synthetic sample data, the generated Customer 360 output contains 6 customers.

Key findings:

- Highest revenue customer: `C005` with `334.99` total revenue.
- Customers flagged as churn risk: `C003` and `C006`.
- Churn-risk pattern in this demo: customers with only 1 completed order, no checkout events, and a high-priority support ticket are marked as churn risk.
- Returned orders are excluded from revenue. For example, customer `C003` had a returned order of `210.00`, so only the completed order of `33.75` is counted in total revenue.
- Gold loyalty customers, `C001` and `C005`, generated the strongest revenue in this sample.
- The model workflow writes `churn_model.joblib` and `model_metrics.json`. The reported metrics are only a technical workflow check because the dataset is intentionally tiny and synthetic.

## Stack Demonstrated

- Python: maintainable package structure, reusable classes, clean CLI
- SQL: staging, aggregation, and mart logic
- Pandas / NumPy: data ingestion and feature preparation
- SQLite locally, with Snowflake-flavored migration SQL included
- pytest: unit, integration, and schema validation tests
- ML workflow: SageMaker-style training script and model artifact output

## Project Structure

```text
customer360-data-engineering-demo/
  data/raw/                  # realistic sample source data
  docs/problem_set.md         # business questions and expected outcomes
  sql/                        # warehouse transformations and migration SQL
  src/customer360/            # pipeline, validation, and ML code
  tests/                      # unit and integration tests
```

## Quick Start

```powershell
cd customer360-data-engineering-demo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m customer360.cli build --data-dir data/raw --output-dir build
python -m customer360.ml.train --input build/customer_360.csv --model-dir build
pytest
```

On macOS/Linux, use `source .venv/bin/activate`.

## Role Mapping

- Customer 360 pipeline: `src/customer360/pipeline.py`, `sql/customer_360.sql`
- ML workflow automation: `src/customer360/ml/train.py`
- Hive/Spark to Snowflake migration: `sql/legacy_hive_to_snowflake.sql`
- Clean Python and SQL: typed functions, small modules, clear boundaries
- Testing and validation: `tests/`, `src/customer360/validation.py`

## Example CLI

```powershell
python -m customer360.cli build --data-dir data/raw --output-dir build
python -m customer360.cli validate --customer360 build/customer_360.csv
```

## Notes

This project intentionally avoids requiring AWS or Snowflake credentials. The code is local-first so a reviewer can run it quickly, while the folder names, scripts, and SQL mirror how the same work would be packaged for production cloud workflows.
