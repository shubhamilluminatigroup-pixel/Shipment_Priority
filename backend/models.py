from sqlalchemy import Column, String, Float, Integer, Date, DateTime, Enum, JSON
from database import Base
from datetime import datetime
import uuid
import enum


def generate_uuid():
    return str(uuid.uuid4())


class ShipmentStatus(str, enum.Enum):
    PENDING = "Pending"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    DELAYED = "Delayed"
    CANCELLED = "Cancelled"


class Shipment(Base):
    __tablename__ = "shipments"

    shipment_id = Column(String, primary_key=True, default=generate_uuid)
    order_id = Column(String, nullable=False)
    customer_id = Column(String, nullable=False)

    origin_address = Column(JSON, nullable=False)
    destination_address = Column(JSON, nullable=False)

    value = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    shelf_life_days = Column(Integer, nullable=False)
    delivery_date = Column(Date, nullable=False)

    shipment_status = Column(Enum(ShipmentStatus), default=ShipmentStatus.PENDING)
    shipment_type = Column(String, nullable=False)  # frozen / normal
    regulatory_flags = Column(JSON, default=list)   # e.g., ["hazmat", "cold_chain"]

    carrier_id = Column(String, nullable=False)
    vehicle_id = Column(String, nullable=True)

    priority_score = Column(Float, nullable=True)

    pickup_time = Column(DateTime, nullable=True)
    delivery_time = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WeightConfig(Base):
    __tablename__ = "weight_configs"

    feature_name = Column(String, primary_key=True)  # e.g., "value", "weight", etc.
    weight_value = Column(Float, nullable=False, default=0.0)