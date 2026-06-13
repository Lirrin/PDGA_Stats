from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from db_init import Base

class LayoutHole(Base):
    __tablename__ = "bronze_layout_hole"

    id = Column(Integer, primary_key=True, autoincrement=True)

    layout_id = Column(
        Integer,
        ForeignKey("bronze_course_layout.layout_id"),
        nullable=False,
        index=True
    )

    hole_number = Column(Integer, nullable=False)

    hole_par = Column(Integer, nullable=False)
    hole_length = Column(Integer, nullable=False)
    length_unit = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("layout_id", "hole_number", name="uq_layout_hole"),
    )