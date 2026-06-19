import pandas as pd
from pathlib import Path
from dataclasses import fields
from pdga_scraper.export.to_database import serialize_payload, build_staging_rows
import csv
import os
import json


def csv_writer(rows_by_table, STAGING_TABLES, folder_path="TestOutputs"):
    for name, config in STAGING_TABLES.items():
        rows = rows_by_table.get(name)
        if rows is None:
            continue

        file_path = os.path.join(folder_path, f"{name}.csv")

        if not rows:
            continue

        key_fields = config["key_fields"]

        base_fields = key_fields + ["source", "payload"]

        fieldnames = base_fields

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            for row in rows:
                writer.writerow(row)

def csv_reader(folder_path, STAGING_TABLES):
    """
    Reads staging CSVs and rebuilds rows_by_table format:

    rows_by_table[name] = [
        {"key1": ..., "key2": ..., "source": ..., "payload": {...}},
    ]
    """

    rows_by_table = {}

    for name, config in STAGING_TABLES.items():

        file_path = os.path.join(folder_path, f"{name}.csv")

        if not os.path.exists(file_path):
            continue

        key_fields = config["key_fields"]

        rows = []

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:

                # --- rebuild row dict ---
                rebuilt = {}

                # keys
                try:
                    for k in key_fields:
                        rebuilt[k] = row[k]
                except KeyError as e:
                    raise ValueError(
                        f"Missing key field {e} in CSV for '{name}'"
                    )

                # source (optional fallback)
                rebuilt["source"] = row.get("source")

                # payload (must be valid JSON string in CSV)
                try:
                    rebuilt["payload"] = row["payload"] #keep as json string
                except Exception as e:
                    raise ValueError(
                        f"Invalid JSON payload in '{name}' CSV row: {row['payload']}"
                    ) from e

                rows.append(rebuilt)

        rows_by_table[name] = rows

    return rows_by_table