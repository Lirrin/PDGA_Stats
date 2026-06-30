import json
from pdga_scraper.database.staging.create_table.create_staging_event_division import StagingEventDivision
from pdga_scraper.database.bronze.create_table.create_bronze_division import BronzeDivision
from pdga_scraper.database.db_init import SessionLocal, engine
from datetime import datetime, timezone


def reset_bronze_division(session, division_ids = None, full_reset=False):
    """
    Manual reset only
    Resets bronze
    """

    if full_reset and division_ids:
        raise ValueError("Choose either full_rest or division_ids, not both")

    # FULL RESET (DANGER)
    if full_reset:
        session.query(BronzeDivision).delete()

        session.commit()
        print("FULL RESET COMPLETE")
        return

    # Targeted Reset
    if division_ids:
        session.query(BronzeDivision).filter(
            BronzeDivision.division_id.in_(division_ids)
        ).delete(synchronize_session=False)

        session.commit()
        print(f"RESET COMPLETE FOR {len(division_ids)} divisions")
        return
    
    raise ValueError("Must provide division ids or full_reset=True")

def build_bronze_division(payload):
    return BronzeDivision(
        division_id = payload["division_id"],
        division_code = payload["division_code"],
        division_name = payload["division_name"],
        is_pro = payload["is_pro"]
    )

def load_bronze_division(session, status_filter=("pending",)):

    staging_divisions = (
        session.query(StagingEventDivision.division_id)
        .filter(StagingEventDivision.status.in_(status_filter))
        .filter(StagingEventDivision.division_id.isnot(None))
        .distinct()
        .all()
    )

    existing = {
        r[0] for r in session.query(BronzeDivision.division_id).all()
    }

    for (division_id,) in staging_divisions:

        if division_id in existing:
            continue

        staging = (
            session.query(StagingEventDivision)
            .filter(StagingEventDivision.division_id == division_id)
            .order_by(StagingEventDivision.id)
            .first()
        )

        if not staging:
            continue

        payload = json.loads(staging.payload)
        bronze_division = build_bronze_division(payload)
        session.add(bronze_division)

        existing.add(division_id)  # prevents duplicates within same run

    session.commit()

    print("Bronze Division load complete.")

if __name__ == "__main__":
    session = SessionLocal()
    print("Running Load Bronze Division")
    load_bronze_division(session)
    #reset_bronze_division(session, full_reset=True)
    print('Done')
    session.close()