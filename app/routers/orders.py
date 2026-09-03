from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Order,
    OrderItem,
    Product,
    Cart,
    CartItem,
)
from app.schemas import OrderCreate, OrderResponse
from app.dependencies import get_current_user, get_current_admin


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# =========================================================
# CREATE ORDER
# =========================================================

@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if not order_data.items:
        raise HTTPException(
            status_code=400,
            detail="Order must contain at least one item"
        )

    total_price = 0

    # Validate products and stock
    for item in order_data.items:

        if item.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantity must be greater than 0"
            )

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.name}"
            )

        total_price += product.price * item.quantity

    # Create order
    new_order = Order(
        user_id=current_user.id,
        total_price=total_price,
        status="pending"
    )

    db.add(new_order)
    db.flush()

    # Create order items and reduce stock
    for item in order_data.items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)

        product.quantity -= item.quantity

    db.commit()
    db.refresh(new_order)

    return new_order


# =========================================================
# MY ORDERS
# =========================================================

@router.get(
    "/",
    response_model=list[OrderResponse]
)
def get_my_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Order).filter(
        Order.user_id == current_user.id
    ).all()


# =========================================================
# ORDER HISTORY
# IMPORTANT: Must be BEFORE /{order_id}
# =========================================================

@router.get(
    "/history",
    response_model=list[OrderResponse]
)
def get_order_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Order).filter(
        Order.user_id == current_user.id
    ).order_by(Order.id.desc()).all()


# =========================================================
# CHECKOUT CART
# IMPORTANT: Must be BEFORE /{order_id}
# =========================================================

@router.post(
    "/checkout",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def checkout(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Get user's cart
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    # Get cart items
    cart_items = db.query(CartItem).filter(
        CartItem.cart_id == cart.id
    ).all()

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total_price = 0

    # Validate cart
    for item in cart_items:

        if item.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid cart quantity"
            )

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

        total_price += product.price * item.quantity

    # Create order
    order = Order(
        user_id=current_user.id,
        total_price=total_price,
        status="pending"
    )

    db.add(order)
    db.flush()

    # Create order items
    for item in cart_items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)

        # Reduce stock
        product.quantity -= item.quantity

    # Clear cart
    for item in cart_items:
        db.delete(item)

    db.commit()
    db.refresh(order)

    return order


# =========================================================
# ADMIN - GET ALL ORDERS
# IMPORTANT: Must be BEFORE /{order_id}
# =========================================================

@router.get(
    "/admin/all",
    response_model=list[OrderResponse]
)
def get_all_orders(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return db.query(Order).order_by(
        Order.id.desc()
    ).all()


# =========================================================
# ADMIN - UPDATE ORDER STATUS
# =========================================================

@router.put(
    "/admin/{order_id}/status",
    response_model=OrderResponse
)
def update_order_status(
    order_id: int,
    status_value: str,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    allowed_statuses = [
        "pending",
        "confirmed",
        "shipped",
        "delivered",
        "cancelled"
    ]

    if status_value not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Use one of: {allowed_statuses}"
        )

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = status_value

    db.commit()
    db.refresh(order)

    return order


# =========================================================
# GET MY SINGLE ORDER
# IMPORTANT: Keep AFTER all static routes
# =========================================================

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# =========================================================
# DELETE MY ORDER
# =========================================================

@router.delete(
    "/{order_id}"
)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.status not in ["pending", "cancelled"]:
        raise HTTPException(
            status_code=400,
            detail="Only pending or cancelled orders can be deleted"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted successfully"
    }