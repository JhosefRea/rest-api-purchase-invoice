import httpx

'''
Httpx solo uso para consumir del WS de facturas
'''


class HTTPClient:
    @staticmethod
    def get_client() -> httpx.AsyncClient:
        return httpx.AsyncClient()
