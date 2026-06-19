import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from pdga_scraper.database.db_base import Base

#Staging
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

#Bronze
from pdga_scraper.database.bronze.create_table.create_bronze_course import BronzeCourse
from pdga_scraper.database.bronze.create_table.create_bronze_division import BronzeDivision
from pdga_scraper.database.bronze.create_table.create_bronze_event import BronzeEvent
from pdga_scraper.database.bronze.create_table.create_bronze_event_division import BronzeEventDivision
from pdga_scraper.database.bronze.create_table.create_bronze_event_player import BronzeEventPlayer
from pdga_scraper.database.bronze.create_table.create_bronze_event_round import BronzeEventRound
from pdga_scraper.database.bronze.create_table.create_bronze_layout import BronzeLayout
from pdga_scraper.database.bronze.create_table.create_bronze_layout_hole import BronzeLayoutHole
from pdga_scraper.database.bronze.create_table.create_bronze_layout_sequence import BronzeLayoutSequence
from pdga_scraper.database.bronze.create_table.create_bronze_player import BronzePlayer
from pdga_scraper.database.bronze.create_table.create_bronze_player_hole_score import BronzePlayerHoleScore
from pdga_scraper.database.bronze.create_table.create_bronze_player_round import BronzePlayerRound
from pdga_scraper.database.bronze.create_table.create_bronze_player_round_stat import BronzePlayerRoundStat



# --- Engine ---
engine = create_engine("sqlite:///data/pdga.db", echo=False)

@event.listens_for(engine, "connect")
def enable_sqlite_fks(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

# --- Session factory ---
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """
    Creates all tables registered on Base.metadata
    """

    print(Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)



if __name__ == "__main__":
    init_db()