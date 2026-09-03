from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_admin
from app.models import Product
from app.schemas import ProductCreate, ProductResponse


router = APIRouter(
    prefix="/admin/products",
    tags=["Admin Products"]
)


# =========================
# GET ALL PRODUCTS
# =========================

@router.get(
    "/",
    response_model=list[ProductResponse]
)
def get_all_products(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return db.query(Product).all()


# =========================
# CREATE PRODUCT
# =========================

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
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

    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        quantity=product_data.quantity
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


# =========================
# UPDATE PRODUCT
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

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

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

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.quantity = product_data.quantity

    db.commit()
    db.refresh(product)

    return product


# =========================
# DELETE PRODUCT
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

    # Don't delete products already used in orders
    existing_order_item = db.query(
        Product
    ).join(
        Product.order_items
    ).filter(
        Product.id == product_id
    ).first()

    if existing_order_item:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a product that has been ordered"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }