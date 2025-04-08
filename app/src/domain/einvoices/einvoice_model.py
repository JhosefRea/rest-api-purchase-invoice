from pydantic import BaseModel, Field, EmailStr, field_validator, FieldValidationInfo, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from app.src.domain.einvoices.details.einvoice_details_model import DetailModel


class AddressModel(BaseModel):
    street: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    postCode: Optional[str] = Field(None, min_length=1, max_length=20)
    country: str = Field(..., min_length=1, max_length=50)


class EInvoiceModel(BaseModel):
    id: str = Field(None)
    #createdAt: datetime = Field(default_factory=datetime.now) Serviría para un update_now
    createdAt: Optional[datetime] = Field(None)
    paymentDue: Optional[datetime] = Field(None)
    description: Optional[str] = Field(None, max_length=200)
    paymentTerms: Optional[int] = Field(None, gt=0)
    clientName: Optional[str] = Field(None, max_length=100)
    clientEmail: Optional[EmailStr] = Field(None)
    status: str = Field(max_length=50, default="pending")
    items: Optional[List[DetailModel]] = Field(None)
    total: Optional[float] = Field(None, gt=0)
    senderAddress: Optional[AddressModel] = Field(None)
    clientAddress: Optional[AddressModel] = Field(None)
    einvoiceCatalogs: str = Field(..., max_length=100)
           
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders = {datetime: lambda v: v.isoformat()},  # Serializa `datetime` a ISO8601. No la uso
        ser_json_timedelta='iso8601'#tampoco la uso
    )

#LO siguiente no se usa     
@field_validator('status', mode='before')
def validate_pending(cls, v, info: FieldValidationInfo):
    if v == "pending":
        required_fields = [
            "paymentDue", "description", "paymentTerms", "clientName",
            "clientEmail", "total", "senderAddress", "clientAddress", "items"
        ]
        for field in required_fields:
            if field not in info.data or not info.data[field]:
                raise ValueError(f"Field '{field}' is required when status is 'pending'.")
    return v


