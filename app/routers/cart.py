from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Cart, CartItem, Product
from app.schemas import CartItemCreate, CartItemResponse


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


# =========================
# ADD TO CART
# =========================

@router.post(
    "/",
    response_model=CartItemResponse
)
def add_to_cart(
    data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Find product
    product = db.query(Product).filter(
        Product.id == data.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if data.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    # Find user's cart
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    # Create cart if user doesn't have one
    if not cart:

        cart = Cart(
            user_id=current_user.id
        )

        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Check existing cart item
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == data.product_id
    ).first()

    current_quantity = 0

    if existing_item:
        current_quantity = existing_item.quantity

    # Check total required stock
    if product.quantity < current_quantity + data.quantity:

        raise HTTPException(
            status_code=400,
            detail="Not enough stock"
        )

    # Update existing item
    if existing_item:

        existing_item.quantity += data.quantity

        db.commit()
        db.refresh(existing_item)

        return existing_item

    # Create new cart item
    cart_item = CartItem(
        cart_id=cart.id,
        product_id=data.product_id,
        quantity=data.quantity
    )

    db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart_item


# =========================
# GET MY CART
# =========================

@router.get(
    "/",
    response_model=list[CartItemResponse]
)
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        return []

    return db.query(CartItem).filter(
        CartItem.cart_id == cart.id
    ).all()

# =========================
# UPDATE CART ITEM
# =========================

@router.put(
    "/{cart_item_id}",
    response_model=CartItemResponse
)
def update_cart_item(
    cart_item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    product = db.query(Product).filter(
        Product.id == cart_item.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if quantity > product.quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock"
        )

    cart_item.quantity = quantity

    db.commit()
    db.refresh(cart_item)

    return cart_item


# =========================
# REMOVE FROM CART
# =========================

@router.delete(
    "/{cart_item_id}"
)
def remove_from_cart(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:

        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Item removed from cart"
    }