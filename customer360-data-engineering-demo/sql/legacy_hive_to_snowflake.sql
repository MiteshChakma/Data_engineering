-- Legacy Hive/Spark style table:
-- CREATE EXTERNAL TABLE legacy.customer_orders (
--   customer_id STRING,
--   order_id STRING,
--   order_amount DOUBLE,
--   order_date STRING,
--   status STRING
-- )
-- STORED AS PARQUET
-- LOCATION 'hdfs:///warehouse/customer_orders';

-- Snowflake target model.
CREATE OR REPLACE TABLE analytics.customer_orders (
    customer_id VARCHAR,
    order_id VARCHAR,
    order_amount NUMBER(12, 2),
    order_date DATE,
    status VARCHAR,
    loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Example migration load from an external stage.
COPY INTO analytics.customer_orders (
    customer_id,
    order_id,
    order_amount,
    order_date,
    status
)
FROM (
    SELECT
        $1:customer_id::VARCHAR,
        $1:order_id::VARCHAR,
        $1:order_amount::NUMBER(12, 2),
        TO_DATE($1:order_date::VARCHAR),
        $1:status::VARCHAR
    FROM @raw_migration_stage/customer_orders/
)
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

-- Snowflake aggregation equivalent to a common Spark groupBy job.
CREATE OR REPLACE TABLE analytics.customer_order_features AS
SELECT
    customer_id,
    COUNT_IF(status = 'completed') AS completed_orders,
    SUM(IFF(status = 'completed', order_amount, 0)) AS total_revenue,
    MAX(order_date) AS last_order_date
FROM analytics.customer_orders
GROUP BY customer_id;
