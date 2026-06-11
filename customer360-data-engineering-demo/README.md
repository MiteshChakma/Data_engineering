# Customer 360 Data Engineering Demo

Small, runnable portfolio project that demonstrates the core responsibilities of a junior data engineer working on Customer 360 data products, ML workflow automation, and warehouse migration.

## Problem Set

A retail business has customer, order, web event, and support-ticket data spread across different systems. The analytics team needs a reliable Customer 360 table that can answer:

- Which customers are most valuable?
- Which customers are at risk of churn?
- Which source records are invalid before they enter the data product?
- How would a legacy Hive/Spark table be migrated into a Snowflake model?

## Outcome

The pipeline builds `customer_360` with one row per customer, including revenue, order frequency, web activity, support activity, and churn labels. It also trains a simple churn model locally using the same script shape that can be used as an AWS SageMaker training entrypoint.

Generated outputs:

- `build/customer360.db`: SQLite warehouse with raw, staging, and mart tables
- `build/customer_360.csv`: Customer 360 data product
- `build/model_metrics.json`: churn-model metrics
- `build/churn_model.joblib`: trained scikit-learn model

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
