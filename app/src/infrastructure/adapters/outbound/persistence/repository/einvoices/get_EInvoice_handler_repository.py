from fastapi import HTTPException
from bson import ObjectId
from app.src.application.dtos.einvoice.einvoice_dto import EInvoiceDTO
from app.src.application.ports.input.get_EInvoice_UseCase import GetEInvoiceHandlerUC
from app.src.infrastructure.config.database.database import mongodb
from app.src.infrastructure.config.database.database_WS import wsMongoDB


class GetEInvoiceHandlerRepository(GetEInvoiceHandlerUC):
    def __init__(self):
        self.collection = mongodb.get_collection("e-invoices")
        self.collectionWS = wsMongoDB.get_collection("invoices")


    async def get_einvoice(self, id: str) -> EInvoiceDTO:
        try:
            print("________REPOSITORY_GETBYID_HANDLER: ID_________", id)        
            einvoice_id = ObjectId(id)

            # Buscar en la colección de MongoDB
            einvoice = await self.collection.find_one({"_id": einvoice_id})
            if einvoice:
            # Crear y convertir el dict a instancia DTO
                return EInvoiceDTO(**einvoice)
            
            einvoiceWS = await self.collectionWS.find_one({"_id": einvoice_id})
            if einvoiceWS:
            # Crear y convertir el dict a instancia DTO
                return EInvoiceDTO(**einvoiceWS)
                 
            if not einvoice or einvoiceWS:
                raise HTTPException(status_code=404, detail="einvoice not found")
    
        except Exception as e:
            # Manejo general de excepciones
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
