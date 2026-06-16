from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, Text
from pdga_scraper.database.db_base import Base


class StagingEventPlayer(Base):
    __tablename__ = "staging_event_player"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Business key(s)
    event_id = Column(Integer, nullable=False, index=True)
    pdga_number = Column(Integer, nullable=False, index=True)

    # Metadata
    source = Column(String, nullable=False)
    ingested_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Raw dataclass payload
    payload = Column(Text, nullable=False)

    # Processing fields
    processed_at = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="pending")
    error_message = Column(String, nullable=True)