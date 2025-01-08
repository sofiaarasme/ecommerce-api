from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from config import Base, engine
from modules.product.infrastructure.product_controller import router as product_router
from modules.inventory.infrastructure.inventory_controller import router as inventory_router

# Esto asegura que las tablas de la base de datos se creen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce API",
    description="API desarrollada para gestionar los endpoints de un ECommerce",
    version="1.0.0",
)

@app.get("/test-db", tags=["Database Test Connection"])
async def test_db():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"message": "Connection successful"}
    except Exception as e:
        return {"error": str(e)}
    
app.include_router(product_router, prefix="/products", tags=["Products"])

app.include_router(inventory_router, prefix="/inventories", tags=["Inventory"])