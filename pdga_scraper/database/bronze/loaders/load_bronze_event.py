import json
from pdga_scraper.database.staging.create_table.create_staging_event import StagingEvent
from pdga_scraper.database.bronze.create_table.create_bronze_event import BronzeEvent
from pdga_scraper.database.db_init import SessionLocal, engine
from datetime import datetime, timezone

def reset_bronze(session, event_ids=None, full_reset=False):
    """
    Manual utility only.
    Resets bronze + staging state.

    - full_reset=True → wipes everything (DEV ONLY)
    - event_ids=[...] → targeted reset
    """

    if full_reset and event_ids:
        raise ValueError("Choose either full_reset OR event_ids, not both")

    # -------------------------
    # FULL RESET (danger zone)
    # -------------------------
    if full_reset:
        session.query(BronzeEvent).delete()

        session.query(StagingEvent).update({
            StagingEvent.status: "pending",
            StagingEvent.error_message: None
        })

        session.commit()
        print("FULL RESET COMPLETE")
        return

    # -------------------------
    # TARGETED RESET
    # -------------------------
    if event_ids:
        session.query(BronzeEvent).filter(
            BronzeEvent.event_id.in_(event_ids)
        ).delete(synchronize_session=False)

        session.query(StagingEvent).filter(
            StagingEvent.event_id.in_(event_ids)
        ).update({
            StagingEvent.status: "pending",
            StagingEvent.error_message: None
        }, synchronize_session=False)

        session.commit()
        print(f"RESET COMPLETE for {len(event_ids)} events")
        return

    raise ValueError("Must provide event_ids or full_reset=True")

def build_bronze_event(payload):
    return BronzeEvent(
        event_id = payload["event_id"],

         # names
        event_name = payload["name"],
        name_main = payload["name_main"],
        name_pre = payload["name_pre"],
        name_post = payload["name_post"],

        # dates
        start_date = datetime.strptime(payload["start_date"], "%Y-%m-%d").date(),
        end_date = datetime.strptime(payload["end_date"], "%Y-%m-%d").date(),

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


def load_bronze_event(session, status_filter = ("pending",)):
    """
    Load unprocessed staging events into bronze.
    Insert-only MVP version.
    """

    staging_events = (
        session.query(StagingEvent)
        .filter(StagingEvent.status.in_(status_filter))
        .all()
    )

    processed = 0
    skipped = 0
    errored = 0

    existing_events = {
        row[0]
        for row in session.query(BronzeEvent.event_id).all()
    }

    for staging in staging_events:
        if staging.event_id in existing_events:
            staging.status = "processed"
            staging.processed_at = datetime.now(timezone.utc)
            session.commit()
            skipped += 1
            continue

        try:
            payload = json.loads(staging.payload)
            bronze_event = build_bronze_event(payload)

            session.add(bronze_event)
            session.flush()
            #print("FLUSH OK:", bronze_event.event_id)

            staging.status = "processed"
            staging.processed_at = datetime.now(timezone.utc)
            session.commit() # commits bronze + staging

            processed += 1
            existing_events.add(bronze_event.event_id)

        except Exception as e:
            session.rollback()  # 🔥 THIS is the missing piece

            staging.status = "failed"
            staging.processed_at = datetime.now(timezone.utc)
            staging.error_message = str(e)
            session.commit()
            errored += 1

    session.commit()
    #print("COMMIT DONE")

    print(
        f"BronzeEvent load complete. "
        f"Processed={processed}, Skipped={skipped}, Errored = {errored}"
    )



if __name__ == "__main__":
    session = SessionLocal()
    print("Running Load Bronze Event")
    load_bronze_event(session)
    #reset_bronze(session,full_reset=True)
    print('Done')
    session.close()

