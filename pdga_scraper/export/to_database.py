from dataclasses import asdict, is_dataclass, fields
import json
from pdga_scraper.database.staging.create_table.create_staging_course import StagingCourse
from pdga_scraper.database.staging.create_table.create_staging_event import StagingEvent
from pdga_scraper.database.staging.create_table.create_staging_event_division import StagingEventDivision
from pdga_scraper.database.staging.create_table.create_staging_event_player import StagingEventPlayer
from pdga_scraper.database.staging.create_table.create_staging_event_round import StagingEventRound
from pdga_scraper.database.staging.create_table.create_staging_layout import StagingLayout
from pdga_scraper.database.staging.create_table.create_staging_layout_hole import StagingLayoutHole
from pdga_scraper.database.staging.create_table.create_staging_player import StagingPlayer
from pdga_scraper.database.staging.create_table.create_staging_player_hole_score import StagingPlayerHoleScore
from pdga_scraper.database.staging.create_table.create_staging_player_hole_stat import StagingPlayerHoleStat
from pdga_scraper.database.staging.create_table.create_staging_player_round import StagingPlayerRound
from pdga_scraper.database.staging.create_table.create_staging_player_round_stat import StagingPlayerRoundStat

def build_staging_rows_by_table(datasets, STAGING_TABLES, source="pdga_api"):
    """
    Converts API-style datasets into flat row format used by both:
    - write_staging (DB)
    - csv_writer (CSV)
    """

    rows_by_table = {}

    for name, config in STAGING_TABLES.items():

        dataset = getattr(datasets, name, None)
        if dataset is None:
            continue

        key_fields = config["key_fields"]

        rows = []

        for business_key, obj in dataset.items():

            # --- normalize key ---
            if not isinstance(business_key, tuple):
                business_key = (business_key,)

            if len(business_key) != len(key_fields):
                raise ValueError(
                    f"{name}: expected {len(key_fields)} keys {key_fields}, "
                    f"got {business_key}"
                )

            key_data = dict(zip(key_fields, business_key))

            # --- build row ---
            row = {
                **key_data,
                "source": source,
                "payload": serialize_payload(obj)
            }

            rows.append(row)

        rows_by_table[name] = rows

    return rows_by_table

def build_staging_rows(dataset_dict, key_fields, source="pdga_api"):
    """
    Converts API-style dict dataset into flat staging rows.
    """

    rows = []

    for business_key, obj in dataset_dict.items():

        # normalize key
        if not isinstance(business_key, tuple):
            business_key = (business_key,)

        if len(business_key) != len(key_fields):
            raise ValueError(
                f"Expected {len(key_fields)} keys {key_fields}, "
                f"got {business_key}"
            )

        key_data = dict(zip(key_fields, business_key))

        rows.append({
            **key_data,
            "source": source,
            "payload": serialize_payload(obj)  # or raw obj if you prefer JSON later
        })

    return rows

def serialize_payload(obj):
    if is_dataclass(obj):
        return json.dumps(asdict(obj), default=str)

    raise TypeError(f"Unsupported type: {type(obj)}")



def write_staging(session, rows_by_table, STAGING_TABLES):

    for name, config in STAGING_TABLES.items():

        rows = rows_by_table.get(name)
        if not rows:
            continue

        model = config["model"]
        key_fields = config["key_fields"]

        db_objects = []

        for row in rows:

            # --- safety check: ensure required keys exist ---
            try:
                key_data = {k: row[k] for k in key_fields}
            except KeyError as e:
                raise ValueError(
                    f"Missing key field {e} in dataset '{name}' row: {row}"
                )

            db_objects.append(
                model(
                    **key_data,
                    source=row.get("source"),
                    payload=row["payload"]
                )
            )

        session.add_all(db_objects)

    session.commit()