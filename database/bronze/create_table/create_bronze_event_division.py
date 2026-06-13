from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint
from db_init import Base

class BronzeEventDivision(Base):
    __tablename__ = "bronze_event_division"

    id = Column(Integer, primary_key=True, autoincrement=True)

    event_id = Column(Integer, nullable=False, index=True)
    division_id = Column(Integer, nullable=False, index=True)

    player_count = Column(Integer, nullable=False)
    final_round_code = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "division_id",
            name="uq_event_division"
        ),
    )