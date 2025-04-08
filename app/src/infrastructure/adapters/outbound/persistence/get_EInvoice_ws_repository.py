from fastapi import HTTPException
from typing import Any
from .....application.ports.output.get_EInvoice_OutputPort import EInvoiceGetOutputPort
from ....config.rest.async_client import HTTPClient
from config.env_config import WS_EINVOICES_URL
from config.status_code_enum import HTTPStatusEnum



class EInvoiceRepositoryWS(EInvoiceGetOutputPort):
    async def get_einvoice_ws(self, id: str) -> dict[str, Any]:
        url = f"{WS_EINVOICES_URL}/{id}"
        print("___Respository___WS__GETBYID", url)
        try:
            async with HTTPClient.get_client() as client:
                response = await client.get(url)
                response.raise_for_status()
                einvoice_data = response.json()
                print("persitencia - repositorio WS__________", einvoice_data)
                return einvoice_data 
        except Exception as e:
            raise HTTPException(status_code=HTTPStatusEnum.INTERNAL_SERVER_ERROR.value, detail=f"Error conexión WS: {str(e)}")
