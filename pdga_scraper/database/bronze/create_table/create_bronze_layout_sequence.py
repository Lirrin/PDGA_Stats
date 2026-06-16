from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint, func
from pdga_scraper.database.db_base import Base

class BronzeLayoutSequence(Base):
    __tablename__ = "bronze_layout_sequence"

    id = Column(Integer, primary_key=True, autoincrement=True)

    layout_id = Column(
        Integer,
        ForeignKey("bronze_course_layout.layout_id"),
        nullable=False,
        index=True
    )

    sequence_index = Column(Integer, nullable=False)
    hole_number = Column(Integer, nullable=False)

    etl_created_at = Column(DateTime, server_default=func.now(), nullable=False)

    etl_updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("layout_id", "sequence_index"),
    )