import pandas as pd
import pytest

from customer360.validation import validate_raw_sources


def test_validate_raw_sources_rejects_missing_columns():
    frames = {
        "customers": pd.DataFrame({"customer_id": ["C001"]}),
        "orders": pd.DataFrame(columns=["order_id", "customer_id", "order_date", "order_amount", "status"]),
        "web_events": pd.DataFrame(columns=["event_id", "customer_id", "event_time", "event_type", "session_id"]),
        "support_tickets": pd.DataFrame(
            columns=["ticket_id", "customer_id", "created_at", "category", "priority", "resolved_hours"]
        ),
    }

    with pytest.raises(ValueError, match="customers is missing required columns"):
        validate_raw_sources(frames)
