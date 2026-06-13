from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint, func
from db_init import Base

class BronzeDivision(Base):
    __tablename__ = "bronze_division"

    id = Column(Integer, primary_key=True, autoincrement=True)

    division_id = Column(Integer, nullable=False, unique=True, index=True)

    division_code = Column(String, nullable=False)
    division_name = Column(String, nullable=False)

    is_pro = Column(Boolean, nullable=False)

    etl_created_at = Column(DateTime, server_default=func.now(), nullable=False)

    etl_updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("division_id", name="uq_division_id"),
    )