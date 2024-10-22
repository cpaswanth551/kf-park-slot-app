from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from ..base import Base


class Places(Base):

    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(Text)
    total_slots = Column(Integer, default=30)

    slot = relationship("Slots", back_populates="place")


class Slots(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_number = Column(String)
    price = Column(DECIMAL(10, 2), default=10.00)
    is_booked = Column(Boolean, default=False)
    place_id = Column(Integer, ForeignKey("places.id"))

    place = relationship("Places", back_populates="slot")
    reservations = relationship("Reservations", back_populates="slot")


class Reservations(Base):

    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    reservation_time = Column(DateTime, default=func.now())
    time_reserved = Column(String, default="1")
    phone_number = Column(String, default="0000000000")
    status = Column(String, default="Pending")
    slot_id = Column(Integer, ForeignKey("slots.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", back_populates="reservations")
    slot = relationship("Slots", back_populates="reservations")
