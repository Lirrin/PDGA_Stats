@@ -0,0 +1,37 @@


setup staging tables  -include some basic metadata and write raw json

need to valdiate all fields are 1:1 from dataclass to staging table 
    ^ also validate keys for dicts match the keys expected for staging
    ^ done for event, more likely to be an issue in ruond level stuff


round_info - round_id - Event_Round
player_round - round_id, score_id - Player_Round
tournament_player - event_id, pdga_num - Event_Player
player_scores - round_id, score_id, hole_seq - Player_Hole_Score
players - pdga_num - Player
hole_breakdowns - score_id, hole_seq - merge with Player Hole Score
round_stats - score_id, stat_id - Player_Round_Stat

figure out how to prevent duplicating records in staging - maybe just delete records for now

start running things into staging
    not working **********
    figure out how to read in the csv files and just test writing to staging
    partial commmits shouldn't occur since it runs one commit at the end 

figure out upsert to bronze
    Reqs:
        Can rerun without duplicating
        Partial processing
        can reload bronze without touching api

    Basic Arhitecture
        bronze_loader.py - main driver

        loaders/
            table1_loader.py

        loaders should have etl timestamps