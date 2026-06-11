from pathlib import Path

from customer360.ml.train import train
from customer360.pipeline import Customer360Pipeline


def test_train_writes_model_artifacts(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    result = Customer360Pipeline(project_root / "data" / "raw", tmp_path).run()

    metrics = train(result.customer360_csv, tmp_path)

    assert "accuracy" in metrics
    assert (tmp_path / "churn_model.joblib").exists()
    assert (tmp_path / "model_metrics.json").exists()
