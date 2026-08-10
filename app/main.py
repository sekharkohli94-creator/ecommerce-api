from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.products import router as product_router
from app.routers.orders import router as order_router
from app.routers.payments import router as payment_router
from app.routers.admin_orders import router as admin_order_router

app = FastAPI(
    title="E-Commerce Backend API"
)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(admin_order_router)

@app.get("/")
def home():
    return {"message": "Welcome to E-Commerce API"}