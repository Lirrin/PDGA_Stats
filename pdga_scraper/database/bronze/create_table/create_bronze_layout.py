from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint, DateTime, func
from database.db_base import Base

class BronzeLayout(Base):
    __tablename__ = "bronze_course_layout"

    id = Column(Integer, primary_key=True, autoincrement=True)

    layout_id = Column(Integer, nullable=False, unique=True, index=True)

    # FK added here
    course_id = Column(
        Integer,
        ForeignKey("bronze_course.course_id"),
        nullable=False,
        index=True
    )

    layout_name = Column(String, nullable=False)

    hole_count = Column(Integer, nullable=False)
    course_par = Column(Integer, nullable=False)

    total_length = Column(Integer, nullable=False)
    length_unit = Column(String, nullable=False)

    etl_created_at = Column(DateTime, server_default=func.now(), nullable=False)

    etl_updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("layout_id", name="uq_layout_id"),
    )