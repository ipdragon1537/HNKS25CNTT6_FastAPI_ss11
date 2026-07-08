from database import Base
from sqlalchemy import Boolean, Column, Integer, String


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slot_code = Column(String(50), nullable=False, unique=True)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "slot_code": self.slot_code,
            "zone_name": self.zone_name,
            "max_weight": self.max_weight,
            "is_available": self.is_available,
        }