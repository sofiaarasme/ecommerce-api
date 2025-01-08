from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.reports.report_service import ReportService
from config import get_db
from uuid import UUID

router = APIRouter()

def get_report_service(db: Session = Depends(get_db)) -> ReportService:
    return ReportService(db)

@router.get("/sales/total")
async def get_total_sales(service: ReportService = Depends(get_report_service)):
    return {"total_sales": service.get_total_sales()}

@router.get("/sales/{product_id}")
async def get_sales_by_product(product_id: UUID, service: ReportService = Depends(get_report_service)):
    return {"sales": service.get_sales_by_product(product_id)}

@router.get("/profit/total")
async def get_total_profit(service: ReportService = Depends(get_report_service)):
    return {"total_profit": service.get_total_profit()}

@router.get("/profit/{product_id}")
async def get_profit_by_product(product_id: UUID, service: ReportService = Depends(get_report_service)):
    return {"profit": service.get_profit_by_product(product_id)}

@router.get("/products/top")
async def get_top_selling_products(service: ReportService = Depends(get_report_service)):
    return {"top_selling_products": service.get_top_selling_products()}

@router.get("/customers/top")
async def get_top_customers(service: ReportService = Depends(get_report_service)):
    return {"top_customers": service.get_top_customers()}