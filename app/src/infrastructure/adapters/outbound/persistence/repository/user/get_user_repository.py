from fastapi import HTTPException
from bson import ObjectId
from app.src.application.dtos.user.user_dto import UserDTO
from app.src.application.ports.input.users.get_User_UseCase import GetUserUC
from app.src.infrastructure.config.database.database import mongodb
from app.src.domain.users.user_model import UserModel

class GetUserRepository(GetUserUC):
    def __init__(self):
        self.collection = mongodb.get_collection("users")

    async def get_user(self, id: str) -> UserDTO:
        try:
            # ID es un ObjectId            
            user_id = ObjectId(id)
            # Buscar el usuario en la colección de MongoDB
            user = await self.collection.find_one({"_id": user_id})
        
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Crear y retornar un UserDTO basado en el documento encontrado
            return UserDTO(**user)
    
        except Exception as e:
            # Manejo general de excepciones
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
