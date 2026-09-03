from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductResponse
from app.dependencies import get_current_user, get_current_admin


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# =========================
# GET ALL PRODUCTS
# =========================

@router.get(
    "/",
    response_model=list[ProductResponse]
)
def get_products(
    db: Session = Depends(get_db)
):
    return db.query(Product).all()


# =========================
# SEARCH PRODUCTS
# IMPORTANT: BEFORE /{product_id}
# =========================

@router.get(
    "/search",
    response_model=list[ProductResponse]
)
def search_products(
    name: str = "",
    min_price: float = 0,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):

    if min_price < 0:
        raise HTTPException(
            status_code=400,
            detail="Minimum price cannot be negative"
        )

    if max_price is not None and max_price < 0:
        raise HTTPException(
            status_code=400,
            detail="Maximum price cannot be negative"
        )

    if max_price is not None and max_price < min_price:
        raise HTTPException(
            status_code=400,
            detail="Maximum price cannot be less than minimum price"
        )

    query = db.query(Product)

    # Search by name
    if name:
        query = query.filter(
            Product.name.ilike(f"%{name}%")
        )

    # Minimum price
    query = query.filter(
        Product.price >= min_price
    )

    # Maximum price
    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )

    return query.all()


# =========================
# CREATE PRODUCT
# ADMIN ONLY
# =========================

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    if product_data.price < 0:
        raise HTTPException(
            status_code=400,
            detail="Price cannot be negative"
        )

    if product_data.quantity < 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity cannot be negative"
        )

    existing_product = db.query(Product).filter(
        Product.name == product_data.name
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="Product already exists"
        )

    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        quantity=product_data.quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# =========================
# GET ONE PRODUCT
# =========================

@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# =========================
# UPDATE PRODUCT
# ADMIN ONLY
# =========================

@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    if product_data.price < 0:
        raise HTTPException(
            status_code=400,
            detail="Price cannot be negative"
        )

    if product_data.quantity < 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity cannot be negative"
        )

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.quantity = product_data.quantity

    db.commit()
    db.refresh(product)

    return product


# =========================
# DELETE PRODUCT
# ADMIN ONLY
# =========================

@router.delete(
    "/{product_id}"
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }