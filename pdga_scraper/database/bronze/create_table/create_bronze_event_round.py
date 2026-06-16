from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UniqueConstraint, func
from database.db_base import Base

class BronzeEventRound(Base):
    __tablename__ = "bronze_event_round"

    # surrogate PK
    id = Column(Integer, primary_key=True, autoincrement=True)
    #Business Keys
    event_id = Column(Integer, 
                      ForeignKey("bronze_event.event_id"),
                      index=True, 
                      nullable=False)
    round_id = Column(Integer, index=True, nullable=False)

    #Round Info
    round_code = Column(Integer, nullable=False)
    round_number = Column(Integer, nullable=False)
    is_playoff = Column(Boolean, nullable=True)

    #Division Info
    division_code = Column(String, nullable=False)

    #Pools
    is_pooled = Column(String, nullable=True)

    #Course Info
    course_id = Column(Integer,
                       ForeignKey("bronze_course.course_id"),
                       nullable=False)
    layout_id = Column(Integer,
                       ForeignKey("bronze_layout.layout_id"),
                       nullable=False)
    

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
            "round_id",
            name="uq_event_round"
        ),
    )