from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class Car(BaseModel):
    company_id: str
    brand: Optional[str] = "Unknown"
    name: str
    model: str
    fuel_type: str
    transmission: str
    body_type: str
    seating_capacity: int
    price: float
    mileage_city: float
    mileage_highway: float
    engine_displacement: Optional[int] = 0
    engine_type: str
    max_power: Optional[str] = "N/A"
    max_torque: Optional[str] = "N/A"
    cylinders: int
    valves_per_cylinder: Optional[int] = 4
    drive_type: str
    length: int
    width: int
    height: int
    wheelbase: int
    ground_clearance: int
    boot_space: int
    fuel_tank_capacity: float
    airbags: bool
    abs: bool
    ebd: Optional[bool] = False
    brake_assist: Optional[bool] = False
    power_steering: bool
    automatic_climate_control: bool
    rear_ac_vents: bool
    touch_screen: bool
    bluetooth_connectivity: bool
    usb_ports: int
    speakers: int
    parking_sensors: bool
    rear_camera: bool
    image_url: Optional[str] = None


class CarOut(Car):
    id: str = Field(alias="_id")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def convert_Objectid(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data["id"] = self.convert_Objectid(data["_id"])
        data["company_id"] = self.convert_Objectid(data.get("company_id", "Unknown"))
        return data