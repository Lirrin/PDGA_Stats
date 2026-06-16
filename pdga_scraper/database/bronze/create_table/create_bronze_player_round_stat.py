from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, UniqueConstraint, DateTime, func
from database.db_base import Base

class BronzePlayerRoundStat(Base):
    __tablename__ = "bronze_player_round_stat"

    id = Column(Integer, primary_key=True, autoincrement=True)

    stat_id = Column(Integer, nullable=False, index=True)

    # FK added here
    score_id = Column(
        Integer,
        ForeignKey("bronze_player_round.score_id"),
        nullable=False,
        index=True
    )

    stat_count = Column(Integer, nullable=False)
    stat_opportunity = Column(Integer, nullable=False)
    stat_value = Column(Numeric(precision=12,scale=4), nullable=False)

    etl_created_at = Column(DateTime, server_default=func.now(), nullable=False)

    etl_updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("score_id", "stat_id", name="uq_score_stat_id"),
    )