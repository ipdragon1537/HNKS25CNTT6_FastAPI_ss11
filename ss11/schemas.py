from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator
class ParkingSlotCreate(BaseModel):
    slot_code: str = Field(..., max_length=50, description="Mã vị trí đỗ")
    zone_name: str = Field(..., max_length=255, description="Tên khu vực")
    max_weight: int = Field(..., description="Tải trọng tối đa (kg)")
    @field_validator("zone_name")
    @classmethod
    def validate_zone_name(cls, value: str) -> str:
        cleaned_value = value.strip()
        if len(cleaned_value) < 3:
            raise ValueError("zone_name phải có độ dài tối thiểu là 3 ký tự.")
        return cleaned_value
    @field_validator("max_weight")
    @classmethod
    def validate_max_weight(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("max_weight phải là số nguyên lớn hơn 0.")
        return value
class StandardResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: Any
    path: str
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
    )