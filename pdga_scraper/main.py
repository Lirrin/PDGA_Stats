import argparse
import os
import sys
import traceback
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

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

from pdga_scraper.event_pipeline import pipeline
from pdga_scraper.export.to_csv import csv_writer, csv_reader
from pdga_scraper.export.to_database import write_staging, build_staging_rows, build_staging_rows_by_table
from pdga_scraper.Datasets.datasets import DataSets
from pdga_scraper.database.db_init import SessionLocal


def main(write_db: bool = False, write_csv: bool = False, 
         debug: bool = False, rnd_limit: int = None, event_list=None,
         data_source="pdga_api", test_mode=False, csv_path="TestOutputs"):
    default_events = [
        96407  # fpo playoff + mpo weather cancellation
        ,96408  # has a cut
        ,97336  # pdga major
    ]
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
        "event_divisions": {
            "model": StagingEventDivision,
            "key_fields": ["event_id", "division_id"]
        },
        "layout_holes": {
            "model": StagingLayoutHole,
            "key_fields": ["layout_id", "hole_seq"]
        },
        "tournament_rounds": {
            "model": StagingEventRound,
            "key_fields": ["round_id"]
        },
        "player_rounds": {
            "model": StagingPlayerRound,
            "key_fields": ["round_id", "score_id", "pdga_number"]
        },
        "player_scores": {
            "model": StagingPlayerHoleScore,
            "key_fields": ["round_id", "pdga_number", "hole_sequence"]
        },
        "tournament_player": {
            "model": StagingEventPlayer,
            "key_fields": ["event_id", "pdga_number"]
        },
        "all_players": {
            "model": StagingPlayer,
            "key_fields": ["pdga_number"]
        },
        "player_round_stats": {
            "model": StagingPlayerRoundStat,
            "key_fields": ["score_id", "stat_id"]
        },
        "player_hole_stats": {
            "model": StagingPlayerHoleStat,
            "key_fields": ["score_id", "hole_sequence"]
        }
    }

    if event_list is None:
        event_list = default_events

    datasets = DataSets()
    source = data_source

    if test_mode:
        source = "csv_file"
        rows_by_table = csv_reader(csv_path,STAGING_TABLES)
    else:
        time_start = datetime.now()
        for event_id in event_list:
            try:

                start = datetime.now()
                print(f'Main Calling Pipeline for {event_id} at {start}')

                pipeline(event_id, datasets, debug=debug, round_limit=rnd_limit)

                print(f"Finished {event_id} in {datetime.now() - start}")

            except Exception as e:
                print(f"\n[ERROR] Event {event_id} failed")
                print(f"{type(e).__name__}: {e}")
                traceback.print_exc()
                continue
            
        time_end = datetime.now()
        elapsed = time_end-time_start
        print(f'Total Execution time: {elapsed}.')
        print(f'{len(event_list)} events processed.')
        print(f'Average time: {elapsed/len(event_list)}.')

        rows_by_table = build_staging_rows_by_table(datasets, STAGING_TABLES, source)

    if write_csv:
        csv_writer(rows_by_table, STAGING_TABLES, folder_path=csv_path)

    if write_db:
        session = SessionLocal()
        try:
            write_staging(session, rows_by_table, STAGING_TABLES)
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
    events = [79049,
                78193,
                77764,
                77765,
                78647,
                77766,
                78666,
                78194,
                78271,
                78654]
    main(write_csv=True, write_db=True, debug=True, 
         event_list=events, test_mode=False)