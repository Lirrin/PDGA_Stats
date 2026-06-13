from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint, func, Text
from db_init import Base

class StagingEventDivision(Base):
    __tablename__ = "staging_event_division"

    id = Column(Integer, primary_key=True, autoincrement=True)

    #Business key(s)
    event_id = Column(Integer, nullable=True, index=True)
    division_id = Column(Integer, nullable=True, index=True)

    # Metadata
    source = Column(String, nullable=False)
    ingested_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Raw dataclass payload
    payload = Column(Text, nullable=False)

    #Processing fields
    processed_at = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="pending")
    error_message = Column(String, nullable=True)