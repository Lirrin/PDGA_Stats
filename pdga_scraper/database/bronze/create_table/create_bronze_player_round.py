from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func, UniqueConstraint
from database.db_base import Base


class BronzePlayerRound(Base):
    __tablename__ = "bronze_player_round"

    id = Column(Integer, primary_key=True, autoincrement=True)

    round_id = Column(Integer, nullable=False, index=True)
    score_id = Column(Integer, nullable=False, index=True)

    pdga_number = Column(
        Integer,
        ForeignKey("bronze_player.pdga_number"),
        nullable=False,
        index=True
    )

    round_number = Column(Integer, nullable=False)
    is_playoff = Column(Boolean, nullable=False)

    pool = Column(String, nullable=True)
    card_number = Column(Integer, nullable=True)
    tee_time = Column(String, nullable=True)

    place_before_round = Column(Integer, nullable=True)
    place_after_round = Column(Integer, nullable=True)
    is_tied = Column(Boolean, nullable=True)

    round_rating = Column(Integer, nullable=True)
    is_complete = Column(Boolean, nullable=True)

    total_score_before_round = Column(Integer, nullable=True)
    round_score = Column(Integer, nullable=True)
    total_score_after_round = Column(Integer, nullable=True)

    round_to_par = Column(Integer, nullable=True)
    to_par_after_round = Column(Integer, nullable=True)

    etl_created_at = Column(DateTime, server_default=func.now(), nullable=False)

    etl_updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "round_id",
            "score_id",
            "pdga_number",
            name="uq_player_round"
        ),
    )