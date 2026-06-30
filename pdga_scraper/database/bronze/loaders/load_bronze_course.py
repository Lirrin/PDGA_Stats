import json
from pdga_scraper.database.staging.create_table.create_staging_course import StagingCourse
from pdga_scraper.database.bronze.create_table.create_bronze_course import BronzeCourse
from pdga_scraper.database.db_init import SessionLocal, engine
from datetime import datetime, timezone


def reset_bronze_course(session, course_ids = None, full_reset=False):
    """
    Manual reset only
    Resets bronze + staging state
    """

    if full_reset and course_ids:
        raise ValueError("Choose either full_rest or course_ids, not both")

    # FULL RESET (DANGER)
    if full_reset:
        session.query(BronzeCourse).delete()

        session.query(StagingCourse).update({
            StagingCourse.status: "pending",
            StagingCourse.error_message: None,
            StagingCourse.processed_at: None
        })

        session.commit()
        print("FULL RESET COMPLETE")
        return

    # Targeted Reset
    if course_ids:
        session.query(BronzeCourse).filter(
            BronzeCourse.course_id.in_(course_ids)
        ).delete(synchronize_session=False)

        session.query(StagingCourse).filter(
            StagingCourse.course_id.in_(course_ids)
        ).update({
            StagingCourse.status: "pending",
            StagingCourse.error_message: None,
            StagingCourse.processed_at: None
        }, synchronize_session=False)

        session.commit()
        print(f"RESET COMPLETE FOR {len(course_ids)} courses")
        return
    
    raise ValueError("Must provide course ids or full_reset=True")

def build_bronze_course(payload):
    return BronzeCourse(
        course_id = payload["course_id"],
        course_name = payload["course_name"]
    )

def load_bronze_course(session, status_filter = ("pending",)):
    """
    Load unprocessed staging courses into bronze
    Insert-only MVP version
    """

    staging_courses = (
        session.query(StagingCourse)
        .filter(StagingCourse.status.in_(status_filter))
        .filter(StagingCourse.course_id.isnot(None))
        .all()
    )

    processed = 0
    skipped = 0
    errored = 0

    existing_courses = {
        row[0]
        for row in session.query(BronzeCourse.course_id).all()
    }

    for staging in staging_courses:
        if staging.course_id in existing_courses:
            staging.status = "processed"
            staging.processed_at = datetime.now(timezone.utc)
            session.commit()
            skipped += 1
            continue

        try:
            payload = json.loads(staging.payload)
            bronze_course = build_bronze_course(payload)
            session.add(bronze_course)
            session.flush()

            staging.status = "processed"
            staging.processed_at = datetime.now(timezone.utc)
            session.commit()

            processed += 1
            existing_courses.add(bronze_course.course_id)

        except Exception as e:
            session.rollback()

            staging.status = "failed"
            staging.processed_at = datetime.now(timezone.utc)
            staging.error_message = str(e)
            session.commit()
            errored += 1

    session.commit()

    print(
        f"BronzeCourse load complete. "
        f"Processed={processed}, Skipped={skipped}, Errored = {errored}"
    )

if __name__ == "__main__":
    session = SessionLocal()
    print("Running Load Bronze Course")
    load_bronze_course(session)
    #reset_bronze_course(session, full_reset=True)
    print("Done")
    session.close()



