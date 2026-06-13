from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from db_init import Base

class LayoutHoleSequence(Base):
    __tablename__ = "bronze_layout_hole_sequence"

    id = Column(Integer, primary_key=True, autoincrement=True)

    layout_id = Column(
        Integer,
        ForeignKey("bronze_course_layout.layout_id"),
        nullable=False,
        index=True
    )

    sequence_index = Column(Integer, nullable=False)
    hole_number = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("layout_id", "sequence_index"),
    )