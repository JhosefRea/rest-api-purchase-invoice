from pydantic import BaseModel, Field

class ReportEInvoiceCatalogDTO(BaseModel):
    catalogs: str = Field(..., min_length=1, max_length=50)
    cantidad: int = Field(..., gt=0)    
    total: float = Field(..., gt=0)    

    class Config:
        populate_by_name = True # Permite usar tanto alias como nombres originales en DTO
        arbitrary_types_allowed = True