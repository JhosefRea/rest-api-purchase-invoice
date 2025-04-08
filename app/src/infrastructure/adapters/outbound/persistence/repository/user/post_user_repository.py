from passlib.context import CryptContext
from fastapi import HTTPException


from app.src.application.dtos.user.user_dto import UserDTO
from app.src.application.ports.input.users.post_User_UseCase import PostUserUC
from app.src.infrastructure.config.database.database import mongodb
from app.src.domain.users.user_model import UserModel


# Configuración de passlib para usar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    """Hashea la contraseña usando bcrypt."""
    return pwd_context.hash(password)

class PostUserRepository(PostUserUC):
    def __init__(self):
        self.collection = mongodb.get_collection("users")

    async def post_user(self, user: UserModel) -> UserDTO:
       # Preparar el dict para MongoDB (incluye agregar _id a los items si no existen)
        user_dict = self._prepare_user_dict(user)

        # Verificar si el email ya está en la base de datos
        existing_user = await self.collection.find_one({"email": user.email})
    
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        #Hashear la contraseña antes de guardarla
        hashed_password = hash_password(user_dict["password"])
        user_dict["password"] = hashed_password

        # Inserta el documento en la base de datos
        result = await self.collection.insert_one(user_dict)

        # Actualiza el dict con el _id generado por MongoDB para el documento principal
        user_dict["_id"] = str(result.inserted_id)

        # Retorna un InvoicePostDTO basado en el documento almacenado
        return UserDTO(**user_dict)

    def _prepare_user_dict(self, user: UserModel | dict) -> dict:
        # Convertir a dict si es un modelo
        if isinstance(user, UserModel):
            user_dict = user.model_dump(by_alias=True)
        else:
            user_dict = user

        return user_dict

