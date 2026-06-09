from event_pipeline import pipeline
from export.to_csv import csv_writer
from Datasets.datasets import DataSets
import traceback
from datetime import datetime

event_list = [96407, # fpo playoff + mpo weather cancellation
              96408, #has a  cut
              97336 # pdga major
              ] # placeholder

debug = True
datasets = DataSets()
for event_id in event_list:
    try:
        if debug:
            start = datetime.now()
            print(f'Main Calling Pipeline for {event_id} at {start}')
        pipeline(event_id, datasets, debug=debug)
        if debug:
            print(f"Finished {event_id} in {datetime.now() - start}")
    except Exception as e:
        print(f"\n[ERROR] Event {event_id} failed")
        print(f"{type(e).__name__}: {e}")
        traceback.print_exc()
        continue

csv_writer(datasets)