import argparse
from event_pipeline import pipeline
from export.to_csv import csv_writer
from export.to_database import write_staging
from Datasets.datasets import DataSets
from database.db_init import SessionLocal
import traceback
from datetime import datetime


def main(write_db: bool = False, write_csv: bool = False, 
         debug: bool = False, rnd_limit: int = None, event_list=None):
    default_events = [
        96407,  # fpo playoff + mpo weather cancellation
        96408,  # has a cut
        97336,  # pdga major
    ]

    if event_list is None:
        event_list = default_events

    datasets = DataSets()

    for event_id in event_list:
        try:
            if debug:
                start = datetime.now()
                print(f'Main Calling Pipeline for {event_id} at {start}')

            pipeline(event_id, datasets, debug=debug, round_limit=rnd_limit)

            if debug:
                print(f"Finished {event_id} in {datetime.now() - start}")

        except Exception as e:
            print(f"\n[ERROR] Event {event_id} failed")
            print(f"{type(e).__name__}: {e}")
            traceback.print_exc()
            continue

    if write_csv:
        csv_writer(datasets)

    if write_db:
        session = SessionLocal()
        try:
            write_staging(session, datasets)
        finally:
            session.close()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Run PDGA scrapers')
    # parser.add_argument('--write-db', action='store_true', help='Write datasets to staging DB')
    # parser.add_argument('--write-csv', action='store_true', help='Write datasets to CSV')
    # parser.add_argument('--no-debug', dest='debug', action='store_false', help='Disable debug prints')
    # parser.add_argument('--rnd-limit', type=int, default=15, help='Round limit for pipeline')
    # parser.add_argument('--events', nargs='+', type=int, help='Event ids to run (space separated)')
    # args = parser.parse_args()

    # main(write_db=args.write_db, write_csv=args.write_csv, debug=args.debug, rnd_limit=args.rnd_limit, event_list=args.events)

    main(write_db=True)