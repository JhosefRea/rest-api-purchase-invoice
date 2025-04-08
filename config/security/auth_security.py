'''
from fastapi.security import OAuth2PasswordBearer

# esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")
'''


from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
import secrets
from datetime import datetime, timedelta


# Clase de configuración para la seguridad
class SecuritySettings:
    SECRET_KEY = secrets.token_urlsafe(32)  # Genera una clave secreta segura
    ALGORITHM = "HS256"  # Algoritmo para los JWT
    ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Expiración del token en minutos



# Función para crear el token JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=SecuritySettings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SecuritySettings.SECRET_KEY, algorithm=SecuritySettings.ALGORITHM)
    return encoded_jwt

# Esquema Bearer para la seguridad de las rutas
http_bearer = HTTPBearer()

# Función para verificar el token en rutas protegidas
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SecuritySettings.SECRET_KEY, algorithms=[SecuritySettings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return email
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")


