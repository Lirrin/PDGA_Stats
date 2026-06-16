from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from pdga_scraper.database.db_base import Base


class BronzePlayer(Base):
    __tablename__ = "bronze_player"

    id = Column(Integer, primary_key=True, autoincrement=True)

    pdga_number = Column(Integer, nullable=False, unique=True, index=True)

    full_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    home_city = Column(String, nullable=True)
    home_state = Column(String, nullable=True)
    home_country = Column(String, nullable=True)
    home_location = Column(String, nullable=True)

    nationality = Column(String, nullable=True)

    etl_created_at = Column(DateTime, server_default=func.now(), nullable=False)

    etl_updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )