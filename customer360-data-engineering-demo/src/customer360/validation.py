from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "customers": {"customer_id", "email", "signup_date", "signup_channel", "loyalty_tier", "country"},
    "orders": {"order_id", "customer_id", "order_date", "order_amount", "status"},
    "web_events": {"event_id", "customer_id", "event_time", "event_type", "session_id"},
    "support_tickets": {"ticket_id", "customer_id", "created_at", "category", "priority", "resolved_hours"},
}

CUSTOMER360_COLUMNS = {
    "customer_id",
    "signup_date",
    "signup_channel",
    "loyalty_tier",
    "country",
    "completed_orders",
    "total_revenue",
    "returned_orders",
    "web_events",
    "web_sessions",
    "checkout_events",
    "support_tickets",
    "avg_resolution_hours",
    "had_high_priority_ticket",
    "churn_label",
}


def validate_raw_sources(frames: dict[str, pd.DataFrame]) -> None:
    for table_name, required in REQUIRED_COLUMNS.items():
        if table_name not in frames:
            raise ValueError(f"Missing source table: {table_name}")
        _require_columns(table_name, frames[table_name], required)

    orders = frames["orders"]
    if (orders["order_amount"] < 0).any():
        raise ValueError("orders.order_amount must be non-negative")

    valid_statuses = {"completed", "returned"}
    invalid_statuses = set(orders["status"]) - valid_statuses
    if invalid_statuses:
        raise ValueError(f"Invalid order status values: {sorted(invalid_statuses)}")


def validate_customer360_file(path: Path) -> None:
    frame = pd.read_csv(path)
    _require_columns("customer_360", frame, CUSTOMER360_COLUMNS)
    if frame["customer_id"].duplicated().any():
        raise ValueError("customer_360 must contain one row per customer")
    if frame["churn_label"].isna().any():
        raise ValueError("churn_label cannot be null")
    if not set(frame["churn_label"]).issubset({0, 1}):
        raise ValueError("churn_label must be binary")


def _require_columns(table_name: str, frame: pd.DataFrame, required: set[str]) -> None:
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{table_name} is missing required columns: {sorted(missing)}")
