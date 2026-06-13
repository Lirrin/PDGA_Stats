from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint
from db_init import Base


class Event(Base):
    __tablename__ = "bronze_event"

    # surrogate PK
    id = Column(Integer, primary_key=True, autoincrement=True)

    # natural key (PDGA)
    event_id = Column(Integer, unique=True, index=True, nullable=False)

    # names
    name = Column(String, nullable=False)
    name_main = Column(String, nullable=True)
    name_pre = Column(String, nullable=True)
    name_post = Column(String, nullable=True)

    # dates
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    # location
    location_full = Column(String, nullable=False)
    location_short = Column(String, nullable=False)
    country = Column(String, nullable=False)

    # tournament metadata
    tier_code = Column(String, nullable=False)
    tier_name = Column(String, nullable=False)

    td_name = Column(String, nullable=False)
    td_pdga_number = Column(Integer, nullable=False)

    time_zone = Column(String, nullable=False)
    scoring_format = Column(String, nullable=False)

    is_x_tier = Column(Boolean, nullable=False)

    __table_args__ = (
        UniqueConstraint("event_id", name="uq_event_pdga_id"),
    )