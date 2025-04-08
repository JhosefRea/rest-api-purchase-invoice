from fastapi import HTTPException
from app.src.application.dtos.report.report_einvoice_x_catalog_dto import ReportEInvoiceCatalogDTO
from app.src.application.ports.input.reports.report_EInvoice_catalog_UseCase import ReportEInvoiceCatalogUC
from app.src.infrastructure.config.database.database import mongodb


class ReportEinvoiceCatalogRepository(ReportEInvoiceCatalogUC):
    def __init__(self):
        self.collection = mongodb.get_collection("e-invoices") # No reconoce a collection en el método asíncrono

    async def report_einvoices_catalog_Agregations() -> list[ReportEInvoiceCatalogDTO]:
        try: 
            # Definimos el pipeline de agregación para MongoDB
            pipeline = [
                {
                    '$addFields': {
                    'einvoiceCatalogs': {'$ifNull': ['$einvoiceCatalogs', 'Unknown']}
                    }
                },
                {
                    '$group': {
                        '_id': '$einvoiceCatalogs',  # Agrupamos por el campo 'einvoiceCatalogs'
                        'cantidad': {
                            '$sum': 1  # Sumamos 1 por cada documento
                        },
                        'total': {
                            '$sum': {
                                '$ifNull': [
                                    '$total', 0  # Si 'total' es nulo, lo tratamos como 0
                                ]
                            }
                        }
                    }
                },
                {
                    '$project': {
                        'einvoiceCatalogs': '$_id',  # Proyectamos el '_id' como 'catalog'
                        'cantidad': 1,      # Proyectamos 'cantidad'
                        'total': 1,         # Proyectamos 'total'
                        '_id': 0            # Excluimos '_id' del resultado
                    }
                }
            ]

            # Ejecutamos la agregación en la colección de MongoDB
            async_cursor = mongodb.get_collection("e-invoices").aggregate(pipeline)

            # Inicializamos la lista donde almacenaremos los resultados
            result = []

            # Iteramos sobre los documentos devueltos por la agregación
            async for doc in async_cursor:
                # Creamos objetos DTO a partir de los resultados de la agregación
                print("**Repository Report EINVOICE BUCLE FOR**", doc)
                result.append(ReportEInvoiceCatalogDTO(
                    catalogs=doc['einvoiceCatalogs'],
                    cantidad=doc['cantidad'],
                    total=doc['total']
                ))

            # Retornamos la lista de objetos DTO
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error aggregations e-invoices: {str(e)}")    


  
        

    