from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint, func
from db_base import Base

class BronzeEventDivision(Base):
    __tablename__ = "bronze_event_division"

    id = Column(Integer, primary_key=True, autoincrement=True)

    event_id = Column(Integer, nullable=False, index=True)
    division_id = Column(Integer, nullable=False, index=True)

    player_count = Column(Integer, nullable=False)
    final_round_code = Column(Integer, nullable=False)

    etl_created_at = Column(DateTime, server_default=func.now(), nullable=False)

    etl_updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "division_id",
            name="uq_event_division"
        ),
    )