import pandas as pd
from pathlib import Path
from dataclasses import fields
from pdga_scraper.export.to_database import serialize_payload
import csv
import os

def csv_writer(datasets, STAGING_TABLES, folder_path = "TestOutputs", source="pdga_api"):
    """
    file_path_map: dict like {"courses": "courses.csv", ...}
    datasets: same object used in db_writer (attributes per dataset)
    """

    for name, config in STAGING_TABLES.items():
        dataset = getattr(datasets, name, None)
        if dataset is None:
            continue

        file_path = os.path.join(folder_path, f"{name}.csv")

        if not file_path:
            raise ValueError(f"No file path provided for dataset '{name}'")

        key_fields = config["key_fields"]
        expected_key_count = len(key_fields)

        rows = []

        for business_key, obj in dataset.items():

            # --- normalize key ---
            if not isinstance(business_key, tuple):
                business_key = (business_key,)

            if len(business_key) != expected_key_count:
                raise ValueError(
                    f"Dataset '{name}' expected {expected_key_count} keys for {key_fields}, "
                    f"but got {len(business_key)}: {business_key}"
                )

            key_data = dict(zip(key_fields, business_key))

            # --- flatten row ---
            row = {
                **key_data,
                "source": source,
                "payload": serialize_payload(obj)
            }

            rows.append(row)

        # --- write csv ---
        if not rows:
            continue

        fieldnames = list(rows[0].keys())

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)