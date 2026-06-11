from __future__ import annotations

import argparse
from pathlib import Path

from customer360.pipeline import Customer360Pipeline
from customer360.validation import validate_customer360_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Customer 360 data engineering demo")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Build the Customer 360 data product")
    build.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    build.add_argument("--output-dir", type=Path, default=Path("build"))

    validate = subparsers.add_parser("validate", help="Validate an exported Customer 360 CSV")
    validate.add_argument("--customer360", type=Path, required=True)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "build":
        result = Customer360Pipeline(args.data_dir, args.output_dir).run()
        print(f"Customer 360 rows: {result.row_count}")
        print(f"CSV: {result.customer360_csv}")
        print(f"Database: {result.database_path}")
    elif args.command == "validate":
        validate_customer360_file(args.customer360)
        print("Customer 360 schema validation passed")


if __name__ == "__main__":
    main()
