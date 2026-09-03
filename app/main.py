from fastapi import FastAPI

from app.routers import (
    auth,
    products,
    orders,
    payments,
    admin_orders,cart,admin_products,admin_users
)


app = FastAPI(
    title="E-Commerce Backend API",
    version="1.0.0"
)


# =========================
# ROUTERS
# =========================

app.include_router(
    auth.router
)

app.include_router(
    products.router
)

app.include_router(
    orders.router
)

app.include_router(
    payments.router
)

app.include_router(
    admin_orders.router
)
app.include_router(cart.router)
app.include_router(admin_products.router)
app.include_router(admin_users.router)

# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "E-Commerce Backend API is running"
    }