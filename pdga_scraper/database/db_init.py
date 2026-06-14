from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from database.db_base import Base

#Staging
from .staging.create_table.create_staging_course import StagingCourse
from .staging.create_table.create_staging_event_division import StagingEventDivision
from .staging.create_table.create_staging_event import StagingEvent
from .staging.create_table.create_staging_layout_hole import StagingLayoutHole
from .staging.create_table.create_staging_layout import StagingLayout

#Bronze
from .bronze.create_table.create_bronze_course import BronzeCourse
from .bronze.create_table.create_bronze_division import BronzeDivision
from .bronze.create_table.create_bronze_event_division import BronzeEventDivision
from .bronze.create_table.create_bronze_event import BronzeEvent
from .bronze.create_table.create_bronze_layout_hole import BronzeLayoutHole
from .bronze.create_table.create_bronze_layout_sequence import BronzeLayoutSequence
from .bronze.create_table.create_bronze_layout import BronzeLayout



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