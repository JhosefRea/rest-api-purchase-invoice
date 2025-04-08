from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from typing import Any

# Back-end
from app.src.application.services.report_einvoice_x_catalog_service import ReportEinvoiceCatalogService
from app.src.infrastructure.adapters.outbound.persistence.repository.report.report_einvoice_catalog_repository import ReportEinvoiceCatalogRepository


from app.src.application.dtos.report.report_einvoice_x_catalog_dto import ReportEInvoiceCatalogDTO
from app.src.domain.einvoices.einvoice_model import EInvoiceModel


router = APIRouter()

repository_report = ReportEinvoiceCatalogRepository()
service_report = ReportEinvoiceCatalogService(ReportEinvoiceCatalogRepository)


@router.get("/", response_model=list[ReportEInvoiceCatalogDTO])
async def report_einvoices_catalog():
    try:
        reports = await service_report.invoke()
        print("controller________reports", reports)
        if not reports:
            raise HTTPException(status_code=404, detail="No invoices found")
        
        return reports
    
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(e.errors()),
        )