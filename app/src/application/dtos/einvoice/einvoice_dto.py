from pydantic import BaseModel, Field, EmailStr, BeforeValidator, field_validator
from datetime import datetime
from typing import List, Optional, Annotated


from app.src.application.dtos.einvoice.einvoice_address_dto import AddressDTO
from app.src.application.dtos.einvoice.einvoice_details_dto import DetailsDTO 
from config.utils.date_utils import parse_datetime_to_iso_format


PyObjectId = Annotated[str, BeforeValidator(str)]


class EInvoiceDTO(BaseModel):
    mongo_id: Optional[PyObjectId] = Field(alias="_id", default=None)
    id: str = Field(..., min_length=1, max_length=20, example="EC9140")
    createdAt: datetime = Field(..., example="2025-01-22T00:00:00.000Z")
    paymentDue: datetime = Field(..., example="2025-02-21T00:00:00.000Z")
    description: str = Field(..., max_length=200, example="Diseño Gráfico")
    paymentTerms: int = Field(..., gt=0, example=30)
    clientName: str = Field(..., max_length=100, example="Carlos Pérez")
    clientEmail: EmailStr = Field(..., example="carlos.perez@mail.ec")
    status: str = Field(..., max_length=50, example="paid")
    senderAddress: AddressDTO
    clientAddress: AddressDTO
    items: List[DetailsDTO]
    total: float = Field(..., gt=0, example=810.0)
    einvoiceCatalogs: Optional[str] = Field(None, max_length=100) 


    class Config:
        populate_by_name = True # Permite usar tanto alias como nombres originales en DTO
        arbitrary_types_allowed = True
        '''schema_extra = {
            "example": {
                "id": "EC9141",
                "createdAt": "2025-01-22T00:00:00.000Z",
                "paymentDue": "2025-02-21T00:00:00.000Z",
                "description": "Diseño Gráfico",
                "paymentTerms": 30,
                "clientName": "Carlos Pérez",
                "clientEmail": "carlos.perez@mail.ec",
                "status": "paid",
                "senderAddress": {
                    "street": "Av. Amazonas 123",
                    "city": "Quito",
                    "postCode": "170102",
                    "country": "Ecuador"
                },
                "clientAddress": {
                    "street": "Calle Flores 456",
                    "city": "Guayaquil",
                    "postCode": "090101",
                    "country": "Ecuador"
                },
                "items": [
                    {"name": "Diseño de Banners", "quantity": 1, "price": 150},
                    {"name": "Diseño de Correos Electrónicos", "quantity": 2, "price": 180},
                    {"name": "Diseño de Logotipo", "quantity": 1, "price": 300}
                ],
                "total": 810.0
            }
        }'''
    
    @field_validator('createdAt', mode='before')
    @classmethod
    def parse_created_at(cls, value: str) -> datetime:
        return parse_datetime_to_iso_format(value)
        
        
