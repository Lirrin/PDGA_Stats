from event_pipeline import process_event
from export.to_csv import csv_writer

event_list = [96407#, # fpo playoff + mpo weather cancellation
              #96408, #has a  cut
              #97336 # pdga major
              ] # placeholder

debug = True

for event_id in event_list:
    try:
        datasets = process_event(event_id, debug=debug)
    except Exception as e:
        print({
            "event_id": event_id,
            "error": str(e),
            "type": type(e).__name__
        })
        continue

#csv_writer(datasets)