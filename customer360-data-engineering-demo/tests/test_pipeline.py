from pathlib import Path

import pandas as pd

from customer360.pipeline import Customer360Pipeline
from customer360.validation import validate_customer360_file


def test_pipeline_builds_customer360(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    result = Customer360Pipeline(project_root / "data" / "raw", tmp_path).run()

    assert result.row_count == 6
    assert result.database_path.exists()
    assert result.customer360_csv.exists()

    customer360 = pd.read_csv(result.customer360_csv)
    assert customer360["customer_id"].is_unique
    assert customer360.loc[customer360["customer_id"] == "C003", "total_revenue"].item() == 33.75
    assert customer360["churn_label"].isin([0, 1]).all()
    validate_customer360_file(result.customer360_csv)
