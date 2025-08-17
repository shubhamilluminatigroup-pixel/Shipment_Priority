from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date, datetime


class Address(BaseModel):
    street: str
    city: str
    state: str
    pincode: str
    country: str


class ShipmentCreate(BaseModel):
    order_id: str
    customer_id: str
    origin_address: Address
    destination_address: Address

    value: float
    weight: float
    volume: float
    shelf_life_days: int
    delivery_date: date

    shipment_type: Literal["frozen", "normal"]
    regulatory_flags: List[str] = Field(default_factory=list)

    carrier_id: str
    vehicle_id: Optional[str] = None

    pickup_time: Optional[datetime] = None
    delivery_time: Optional[datetime] = None

    priority_score: Optional[float] = None


class Shipment(BaseModel):
    shipment_id: str
    shipment_status: str
    created_at: datetime
    updated_at: datetime
    priority_score: Optional[float] = None
    shelf_life_days: int
    origin_address: Address
    destination_address: Address
    volume: float
    weight: float
    value: float

    class Config:
        orm_mode = True

class FixedWeightConfig(BaseModel):
    value: float = Field(..., ge=0, le=1)
    weight: float = Field(..., ge=0, le=1)
    volume: float = Field(..., ge=0, le=1)
    shelf_life_days: float = Field(..., ge=0, le=1)
    days_to_delivery: float = Field(..., ge=0, le=1)

    class Config:
        schema_extra = {
            "example": {
                "value": 0.25,
                "weight": 0.25,
                "volume": 0.25,
                "shelf_life_days": 0.25,
                "days_to_delivery": 0.25
            }
        }

class WeightConfigItem(BaseModel):
    feature_name: str
    weight_value: float

    class Config:
        orm_mode = True