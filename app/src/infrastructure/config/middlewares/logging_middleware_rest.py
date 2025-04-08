import time
import logging
from fastapi import Request
from typing import Callable

# Instancia para añadir logs/registros de Uvicorn en solicitures y respuestas HTTP 
logger = logging.getLogger("uvicorn")

# Registro de peticiones
async def log_requests(request: Request, call_next: Callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    formatted_process_time = "{0:.2f}".format(process_time * 1000)
    logger.info(f"{request.method} {request.url} completed in {formatted_process_time}ms")
    return response
