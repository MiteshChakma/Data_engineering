# Problem Set

## Business Scenario

The company wants to combine scattered customer data into a Customer 360 data product for analytics and churn prediction. The legacy data platform stores Hive/Spark datasets on-premise, but the future target is Snowflake.

## Source Tables

- `customers.csv`: customer identity, signup channel, and loyalty tier
- `orders.csv`: completed and returned orders
- `web_events.csv`: customer web activity
- `support_tickets.csv`: support case history

## Tasks

1. Validate raw data before loading it into the warehouse.
2. Load the source data into staging tables.
3. Build a Customer 360 mart with customer-level aggregates.
4. Export the mart as a CSV data product.
5. Train a churn model using the exported Customer 360 features.
6. Document how a legacy Hive/Spark dataset would be rewritten for Snowflake.

## Expected Outcome

A reviewer can run the project locally and see a complete miniature data lifecycle: ingestion, validation, transformation, data product creation, model training, and tests.

## Acceptance Criteria

- Every customer appears once in `customer_360`.
- Revenue excludes returned orders.
- Churn labels are binary and never null.
- Schema checks fail fast when required columns are missing.
- Tests cover transformations, validation, and the end-to-end build.
