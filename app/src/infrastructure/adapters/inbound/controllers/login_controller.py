''' 
from fastapi import APIRouter, HTTPException, Depends, FastAPI
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from authx import AuthX
import secrets

# Crear el router de FastAPI
router = APIRouter()

# Configuración de passlib para usar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo Pydantic para el usuario
class User(BaseModel):
    email: EmailStr = Field(..., example="zlatan@empresa.ec")
    password: str = Field(..., example="string")

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    """Hashea la contraseña usando bcrypt."""
    return pwd_context.hash(password)

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)

# Conexión con MongoDB (usando motor)
class MongoDB:
    def __init__(self, db_url: str, db_name: str):
        self.client = AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]

# Inicia la conexión a la base de datos
mongo = MongoDB(db_url="mongodb+srv://root:123@cluster0.wa2sz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", db_name="budget-classification")

# Dependencia para obtener la base de datos
async def get_db() -> AsyncIOMotorDatabase:
    return mongo.db

# Genera una clave secreta segura para usar en JWT
secret_key = secrets.token_urlsafe(32)

# Configuración de AuthX
config = {
    "SECRET_KEY": secret_key,  # Clave secreta para firmar JWT
    "JWT_ALGORITHM": "HS256",  # Algoritmo usado para firmar JWT
    "JWT_ACCESS_TOKEN_EXPIRES": 3600,  # Tiempo de expiración del token de acceso en segundos (ej. 1 hora)
    "JWT_REFRESH_TOKEN_EXPIRES": 86400,  # Tiempo de expiración del token de actualización en segundos (ej. 1 día)
}

# Inicializa AuthX con la configuración
authx = AuthX(config=config)

# Endpoint de login
@router.post("/login")
async def login_user(user: User, db: AsyncIOMotorDatabase = Depends(get_db)):
    # Buscar al usuario en la base de datos
    existing_user = await db.users.find_one({"email": user.email})
    
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verificar la contraseña ingresada con el hash almacenado
    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generar un token de acceso
    access_token = authx.create_access_token({"email": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

    
-------------------------------2DA FORMA OAUTH2 - FORMULARIO --------------------------------

from fastapi import APIRouter, HTTPException, Depends, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from authx import AuthX
import secrets

router = APIRouter()

# Configuración de passlib para usar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo Pydantic para el usuario
class User(BaseModel):
    email: EmailStr = Field(..., example="zlatan@empresa.ec")
    password: str = Field(..., example="string")

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    """Hashea la contraseña usando bcrypt."""
    return pwd_context.hash(password)

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)

# Conexión con MongoDB (usando motor)
class MongoDB:
    def __init__(self, db_url: str, db_name: str):
        self.client = AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]

# Inicia la conexión a la base de datos
mongo = MongoDB(
    db_url="mongodb+srv://root:123@cluster0.wa2sz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    db_name="budget-classification",
)

# Dependencia para obtener la base de datos
async def get_db() -> AsyncIOMotorDatabase:
    return mongo.db

# Clase de configuración para AuthX
class AuthSettings(BaseModel):
    SECRET_KEY: str = secrets.token_urlsafe(32)  # Clave secreta para firmar JWT
    JWT_ALGORITHM: str = "HS256"  # Algoritmo para firmar los tokens JWT
    JWT_ACCESS_TOKEN_EXPIRES: int = 3600  # Tiempo de expiración para tokens de acceso (en segundos)
    JWT_REFRESH_TOKEN_EXPIRES: int = 86400  # Tiempo de expiración para tokens de actualización (en segundos)
    JWT_TOKEN_LOCATION: list[str] = ["headers"]  # Ubicación de los tokens (headers o cookies)
    JWT_COOKIE_CSRF_PROTECT: bool = False  # Desactiva la protección CSRF por defecto
    JWT_COOKIE_SECURE: bool = False  # Desactiva cookies seguras por defecto
    JWT_COOKIE_DOMAIN: str = None  # Define el dominio de las cookies (opcional)
    JWT_ENCODE_AUDIENCE: str = "your_audience"  # Define una audiencia esperada para el token JWT
    JWT_ENCODE_ISSUER: str = "your_issuer"  # **Emisor** del token JWT
    private_key: str = "-----BEGIN PRIVATE KEY-----\nMIIBV...END PRIVATE KEY-----"  # Clave privada en formato PEM

    def has_location(self, location: str) -> bool:
        """Método para verificar si el token tiene una ubicación específica."""
        return location in self.JWT_TOKEN_LOCATION



# Inicializar AuthX con la configuración
authx = AuthX(config=AuthSettings())
from jose import JWTError, jwt
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
# OAuth2PasswordBearer: Para recibir el token en las rutas protegidas
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# Función para verificar si el token es válido
def verify_token(token: str = Depends(oauth2_scheme)):
    print("_____verify_token()______")
    try:
        payload = jwt.decode(token, AuthSettings().SECRET_KEY, algorithms=[AuthSettings().JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Endpoint de login
@router.post("/",)
async def login_user(user: User, db: AsyncIOMotorDatabase = Depends(get_db)):
    print("_____login_user()______")
    # Buscar al usuario en la base de datos
    existing_user = await db.users.find_one({"email": user.email})
    
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verificar la contraseña ingresada con el hash almacenado
    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generar un token de acceso
    access_token = authx.create_access_token(uid=user.email, data={"email": user.email})

    
    return {"access_token": access_token, "token_type": "bearer"}




@router.get("/protected")
async def protected_route(user: Annotated[str, Depends(oauth2_scheme)], db: AsyncIOMotorDatabase = Depends(get_db)):
    print("_____login_user()______")
    # Buscar al usuario en la base de datos
    existing_user = await db.users.find_one({"email": user.email})
    
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verificar la contraseña ingresada con el hash almacenado
    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generar un token de acceso
    access_token = authx.create_access_token(uid=user.email, data={"email": user.email})

    
    return {"access_token": access_token, "token_type": "bearer"}

'''

#------------------------------------3RA FORMA HTTP BEARER - SOLO ACCESS TOKEN -----------------------------------------------------

from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


from config.security.auth_security import verify_token, create_access_token


router = APIRouter()

# Configuración de passlib para usar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo Pydantic para el usuario
class User(BaseModel):
    email: EmailStr = Field(..., example="zlatan@empresa.ec")
    password: str = Field(..., example="string")


# Conexión con MongoDB (usando motor)
class MongoDB:
    def __init__(self, db_url: str, db_name: str):
        self.client = AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]

# Inicia la conexión a la base de datos
mongo = MongoDB(
    db_url="mongodb+srv://root:123@cluster0.wa2sz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    db_name="budget-classification",
)

# Dependencia para obtener la base de datos
async def get_db() -> AsyncIOMotorDatabase:
    return mongo.db

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    """Hashea la contraseña usando bcrypt."""
    return pwd_context.hash(password)

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)




# Endpoint de login
@router.post("/")
async def login_user(user: User, db: AsyncIOMotorDatabase = Depends(get_db)):
    # Buscar al usuario en la base de datos
    existing_user = await db.users.find_one({"email": user.email})
    
    if not existing_user:
        raise HTTPException(status_code=401, detail="Usuario no registrado")
    
    # Verificar la contraseña ingresada con el hash almacenado
    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Generar un token de acceso
    access_token = create_access_token({"sub": user.email})
    
    # Convierte el objeto `existing_user` en un formato serializable (diccionario)
    existing_user["_id"] = str(existing_user["_id"])  # Convierte `ObjectId` a cadena
    
    return {"access_token": access_token, "token_type": "bearer", "user": existing_user}


# Endpoint protegido
@router.get("/protected")
async def protected_route(email: str = Depends(verify_token)):
    return {"message": f"Acceso concedido para el usuario: {email}"}

# Agregar las rutas del router a la aplicación principal
