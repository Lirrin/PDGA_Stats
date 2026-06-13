from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint
from db_init import Base

class BronzeCourse(Base):
    __tablename__ = "bronze_course"

    # surrogate PK
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, unique=True, index=True, nullable=False)
    course_name = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("course_id", name="uq_course_id"),
    )