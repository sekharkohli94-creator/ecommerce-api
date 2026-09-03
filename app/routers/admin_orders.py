from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order,User
from app.schemas import OrderResponse, OrderStatusUpdate
from app.dependencies import get_current_admin


router = APIRouter(
    prefix="/admin/orders",
    tags=["Admin Orders"]
)


# =========================
# GET ALL ORDERS
# =========================

@router.get(
    "/",
    response_model=list[OrderResponse]
)
def get_all_orders(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    orders = db.query(Order).all()

    return orders


# =========================
# GET ONE ORDER
# =========================

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_admin_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order


# =========================
# UPDATE ORDER STATUS
# =========================

@router.put(
    "/{order_id}/status",
    response_model=OrderResponse
)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    valid_statuses = [
        "pending",
        "confirmed",
        "shipped",
        "delivered",
        "cancelled"
    ]

    if status_data.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order status"
        )

    order.status = status_data.status

    try:
        db.commit()
        db.refresh(order)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update order status"
        )

    return order

