import json
from pdga_scraper.database.staging.create_table.create_staging_event import StagingEvent
from pdga_scraper.database.bronze.create_table.create_bronze_event import BronzeEvent
from pdga_scraper.database.db_init import SessionLocal

def build_bronze_event(payload):
    return BronzeEvent(
        event_id = payload["event_id"],

         # names
        event_name = payload["name"],
        name_main = payload["name_main"],
        name_pre = payload["name_pre"],
        name_post = payload["name_post"],

        # dates
        start_date = payload["start_date"],
        end_date = payload["end_date"],

        # location
        location_full = payload["location_full"],
        location_short = payload["location_short"],
        country = payload["country"],

        # tournament metadata
        tier_code = payload["tier_code"],
        tier_name = payload["tier_name"],

        td_name = payload["td_name"],
        td_pdga_number = payload["td_pdga_number"],

        time_zone = payload["time_zone"],
        scoring_format = payload["scoring_format"],

        is_x_tier = payload["is_x_tier"]

    )


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
            try:
                payload = json.loads(staging.payload)
                bronze_event = build_bronze_event(payload)
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

if __name__ == "__main__":
    session = SessionLocal()
    print("Running Load Bronze Event")
    load_bronze_event(session)
    print('Done')
    session.close()