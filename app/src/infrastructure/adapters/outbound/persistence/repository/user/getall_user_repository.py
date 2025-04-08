from fastapi import HTTPException
from app.src.application.dtos.user.user_dto import UserDTO
from app.src.application.dtos.user.user_rol_dto import UserRolDTO
from app.src.application.ports.input.users.getall_User_UseCase import GetAllUserUC
from app.src.infrastructure.config.database.database import mongodb


class GetAllUserRepository(GetAllUserUC):
    def __init__(self):
        self.collection = mongodb.get_collection("users")

    async def get_all_users(self) -> list[UserDTO]:
        documents = await self.collection.find().to_list(100)
        return [self.document_to_invoice(doc) for doc in documents if doc.get("status") == "active"]

    def document_to_invoice(self, document: dict) -> UserDTO:
        user_rol_data = document.get("userRol", {})

        userRol = UserRolDTO(
            rol=user_rol_data.get("rol", "Unknown rol"),
            description=user_rol_data.get("description", "Unknown description"),
        )

        return UserDTO(
            mongo_id=document.get("_id"), #o document["_id"]
            name=document.get("name", "default_user_name"),
            email=document.get("email", "default_user_email@empresa.com"),
            password=document.get("password", "default_user_password"),
            userRol=userRol,
            status=document.get("status", "default_no_encontrado")
        )

    '''async def get_all_user(self) -> list[UserDTO]:
        users = []
        try:
            
            # Buscar todos los usuarios en la colección de MongoDB
            users = await self.collection.find().to_list(1000)
            
            if not users:
                raise HTTPException(status_code=404, detail="Users not found")
            
            # Retornar una lista de UserDTO basados en los documentos encontrados
            user_dtos = [UserDTO(**user) for user in users]

            return user_dtos
    
        except Exception as e:
            # Manejo general de excepciones
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
            '''