from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


FEATURE_COLUMNS = [
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
]

TARGET_COLUMN = "churn_label"


def train(input_path: Path, model_dir: Path) -> dict[str, float]:
    model_dir.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(input_path)

    X = frame[FEATURE_COLUMNS]
    y = frame[TARGET_COLUMN]

    # Tiny demo dataset: stratification is skipped so the workflow remains runnable.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.34, random_state=42)

    categorical = ["signup_channel", "loyalty_tier", "country"]
    numeric = [col for col in FEATURE_COLUMNS if col not in categorical]

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("numeric", "passthrough", numeric),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=50, random_state=42)),
        ]
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]
    metrics = {"accuracy": float(accuracy_score(y_test, predictions))}
    if len(set(y_test)) > 1:
        metrics["roc_auc"] = float(roc_auc_score(y_test, probabilities))

    joblib.dump(model, model_dir / "churn_model.joblib")
    (model_dir / "model_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Train churn model from Customer 360 features")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, default=Path("build"))
    args = parser.parse_args()

    metrics = train(args.input, args.model_dir)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
