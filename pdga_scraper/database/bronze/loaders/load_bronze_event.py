from sqlalchemy.exc import IntegrityError

from pdga_scraper.database.staging.create_table.create_staging_event import StagingEvent
from pdga_scraper.database.bronze.create_table.create_bronze_event import BronzeEvent

def build_bronze_event(payload):
    pass


def load_bronze_event(session):
    """
    Load unprocessed staging events into bronze.
    Insert-only MVP version.
    """

    staging_events = (
        session.query(StagingEvent)
        .filter(StagingEvent.status == "pending")
        .all()
    )

    inserted = 0
    skipped = 0

    existing_events = {
        row[0]
        for row in session.query(BronzeEvent.event_id).all()
    }

    for staging in staging_events:
        if staging.event_id in existing_events:
            staging.status = "processed"
            skipped += 1
            continue
        else:
            payload = staging.payload
            bronze_event = build_bronze_event(payload)

            try:
                session.add(bronze_event)
                session.flush()

                staging.status = "processed"
                inserted += 1
                existing_events.add(bronze_event.event_id)

            except Exception as e:
                staging.status = "failed"
                staging.error_message = str(e)
                

                # already exists in bronze
                skipped += 1

    session.commit()

    print(
        f"BronzeEvent load complete. "
        f"Inserted={inserted}, Skipped={skipped}"
    )