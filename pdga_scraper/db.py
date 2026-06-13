import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'pdga.db'))
engine = create_engine(f"sqlite:///{db_path}", echo=False)

@event.listens_for(engine, "connect")
def _enable_fks(dbapi_conn, conn_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

SessionLocal = sessionmaker(bind=engine)