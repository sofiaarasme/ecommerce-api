from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from config import Base, engine
from modules.product.infrastructure.product_controller import router as product_router
from modules.inventory.infrastructure.inventory_controller import router as inventory_router
from modules.user.infrastructure.user_controller import router as user_router
from modules.carts.infrastructure.car_controller import router as cart_router
from modules.order.infrastructure.order_controller import router as order_router

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

app.include_router(user_router, prefix="/users", tags=["Users"])

app.include_router(cart_router, prefix="/carts", tags=["Carts"])

app.include_router(order_router, prefix="/orders", tags=["Orders"])