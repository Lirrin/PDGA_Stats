from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func, UniqueConstraint
from database.db_base import Base


class BronzeEventPlayer(Base):
    __tablename__ = "bronze_event_player"

    id = Column(Integer, primary_key=True, autoincrement=True)

    event_id = Column(Integer, 
                      ForeignKey("bronze_event.event_id"), 
                      nullable=False, 
                      index=True)

    pdga_number = Column(
        Integer,
        ForeignKey("bronze_player.pdga_number"),
        nullable=False,
        index=True
    )

    division = Column(String, nullable=False)

    player_rating_at_event = Column(Integer, nullable=True)

    won_playoff = Column(Boolean, nullable=True)
    prize = Column(String, nullable=True)
    total_strokes = Column(Integer, nullable=True)

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
            "pdga_number",
            name="uq_event_player"
        ),
    )