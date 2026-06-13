from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
#Examples
#from db.bronze.layout_hole import LayoutHole
#from db.bronze.course import Course
#from db.bronze.course_layout import CourseLayout

from sqlalchemy import event

# --- Engine ---
engine = create_engine("sqlite:///data/pdga.db", echo=False)

@event.listens_for(engine, "connect")
def enable_sqlite_fks(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

# --- Session factory ---
SessionLocal = sessionmaker(bind=engine)

# --- Base (metadata registry) ---
Base = declarative_base()


def init_db():
    """
    Creates all tables registered on Base.metadata
    """
    Base.metadata.create_all(bind=engine)




init_db()