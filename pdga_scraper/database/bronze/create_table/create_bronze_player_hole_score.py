from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint, func
from pdga_scraper.database.db_base import Base

class BronzePlayerHoleScore(Base):
    __tablename__ = "bronze_player_hole_score"

    # surrogate PK
    id = Column(Integer, primary_key=True, autoincrement=True)
    round_id = Column(Integer, index=True, nullable=False)
    pdga_number = Column(
                    Integer, 
                    ForeignKey("bronze_player.pdga_number"),
                    index=True, 
                    nullable=False)

    hole_sequence = Column(Integer, index=True, nullable=False)

    #core score fields
    strokes = Column(Integer, nullable=False)
    par = Column(Integer, nullable=False)
    score_to_par = Column(Integer, nullable=False)

    #hole breakdown fields - all nullable as not everyone gets stats
    driving_landing_zone = Column(String, nullable=True)
    scramble = Column(Boolean, nullable=True)
    green_regulation_zone = Column(String, nullable=True)

    c1x_putts = Column(Integer, nullable=True)
    c1_putts = Column(Integer, nullable=True)
    c2_putts = Column(Integer, nullable=True)

    made_distance = Column(Integer, nullable=True)
    ob_strokes = Column(Integer, nullable=True)
    hazard_strokes = Column(Integer, nullable=True)
    missed_mando_strokes = Column(Integer, nullable=True)
    lost_disc_strokes = Column(Integer, nullable=True)
    penalty_strokes = Column(Integer, nullable=True)



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
            "pdga_number",
            "hole_sequence",
            name="uq_player_hole"
        ),
    )