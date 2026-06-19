import pandas as pd
from pathlib import Path
from dataclasses import fields
from pdga_scraper.export.to_database import serialize_payload, build_staging_rows
import csv
import os



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