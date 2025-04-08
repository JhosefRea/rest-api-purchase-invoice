from fastapi import HTTPException
from typing import Any
from .....application.ports.output.getall_EInvoices_OutputPort import EInvoiceGetAllOutputPort
from ....config.rest.async_client import HTTPClient
from config.env_config import WS_EINVOICES_URL
from config.status_code_enum import HTTPStatusEnum


class EInvoicesRepositoryWS(EInvoiceGetAllOutputPort):
    async def get_einvoices_ws(self) -> list[dict[str, Any]]:
        url = f"{WS_EINVOICES_URL}"

        try:
            async with HTTPClient.get_client() as client:
                response = await client.get(url)
                response.raise_for_status()
                einvoices_data = response.json()
                print("persitencia - repositorio WS________", einvoices_data)
                return einvoices_data  
        except Exception as e:
            raise HTTPException(status_code=HTTPStatusEnum.INTERNAL_SERVER_ERROR.value, detail=f"Error conexión WS: {str(e)}")    