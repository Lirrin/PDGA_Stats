from dataclasses import asdict, is_dataclass, fields
import json
from database.staging.create_table.create_staging_course import StagingCourse
from database.staging.create_table.create_staging_event import StagingEvent
from database.staging.create_table.create_staging_layout import StagingLayout
from database.staging.create_table.create_staging_event_division import StagingEventDivision
from database.staging.create_table.create_staging_layout_hole import StagingLayoutHole


def serialize_payload(obj):
    if is_dataclass(obj):
        return json.dumps(asdict(obj), default=str)

    raise TypeError(f"Unsupported type: {type(obj)}")



def write_staging(session, datasets, source="pdga_api"):

    STAGING_TABLES = {
        "course_layouts": {
            "model": StagingLayout,
            "key_fields": ["layout_id"]
        },
        "courses": {
            "model": StagingCourse,
            "key_fields": ["course_id"]
        },
        "events": {
            "model": StagingEvent,
            "key_fields": ["event_id"]
        },
        "events_divisions": {
            "model": StagingEventDivision,
            "key_fields": ["event_id", "division_id"]
        },
        "layout_holes": {
            "model": StagingLayoutHole,
            "key_fields": ["layout_id", "hole_seq"]
        }

    # tournament_rounds: dict = field(default_factory=dict)
    # player_rounds: dict = field(default_factory=dict)
    # player_scores: dict = field(default_factory=dict)
    # tournament_player: dict = field(default_factory=dict)
    # all_players: dict = field(default_factory=dict)
    # player_round_stats: dict = field(default_factory=dict)
    # player_hole_stats: dict = field(default_factory=dict)
    }

    for name, config in STAGING_TABLES.items():
        dataset = getattr(datasets, name, None)
        if dataset is None:
            continue

        model = config["model"]
        key_fields = config["key_fields"]
        expected_key_count = len(key_fields)
        rows = []

        for business_key, obj in dataset.items():
            if not isinstance(business_key, tuple):
                business_key = (business_key,)

            if len(business_key) != expected_key_count:
                raise ValueError(
                    f"Dataset '{name}' expected {expected_key_count} key values for {key_fields}, "
                    f"but got {len(business_key)}: {business_key}"
                )

            key_data = dict(zip(key_fields, business_key))
            rows.append(
                model(
                    **key_data,
                    source=source,
                    payload=serialize_payload(obj)
                )
            )

        session.add_all(rows)

    session.commit()