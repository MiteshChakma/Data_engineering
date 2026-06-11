from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from customer360.validation import validate_raw_sources


RAW_TABLES = {
    "customers": "customers.csv",
    "orders": "orders.csv",
    "web_events": "web_events.csv",
    "support_tickets": "support_tickets.csv",
}


@dataclass(frozen=True)
class PipelineResult:
    database_path: Path
    customer360_csv: Path
    row_count: int


class Customer360Pipeline:
    def __init__(self, data_dir: Path, output_dir: Path) -> None:
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.database_path = output_dir / "customer360.db"
        self.customer360_csv = output_dir / "customer_360.csv"

    def run(self) -> PipelineResult:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        frames = self._read_sources()
        validate_raw_sources(frames)

        with sqlite3.connect(self.database_path) as conn:
            self._load_raw_tables(conn, frames)
            self._build_customer360(conn)
            customer360 = pd.read_sql_query("SELECT * FROM customer_360 ORDER BY customer_id", conn)

        customer360.to_csv(self.customer360_csv, index=False)
        return PipelineResult(self.database_path, self.customer360_csv, len(customer360))

    def _read_sources(self) -> dict[str, pd.DataFrame]:
        frames = {}
        for table_name, file_name in RAW_TABLES.items():
            path = self.data_dir / file_name
            frames[table_name] = pd.read_csv(path)
        return frames

    @staticmethod
    def _load_raw_tables(conn: sqlite3.Connection, frames: dict[str, pd.DataFrame]) -> None:
        for table_name, frame in frames.items():
            frame.to_sql(table_name, conn, if_exists="replace", index=False)

    @staticmethod
    def _build_customer360(conn: sqlite3.Connection) -> None:
        sql_path = Path(__file__).resolve().parents[2] / "sql" / "customer_360.sql"
        conn.executescript(sql_path.read_text(encoding="utf-8"))
