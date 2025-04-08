from enum import Enum

class HTTPStatusEnum(Enum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401 #Cuando el usuario no está autenticado.
    FORBIDDEN = 403 #usuario está autenticado pero no tiene permiso para acceder al recurso.
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500
