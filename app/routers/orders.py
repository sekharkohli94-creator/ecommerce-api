from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies import get_current_user
from app.database import get_db
from app.models import Order, OrderItem, Product
from app.schemas import OrderCreate, OrderResponse

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# CREATE ORDER
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if not order_data.items:
        raise HTTPException(status_code=400, detail="Order must have items")

    try:
        total_price = 0
        products_data = []

        for item in order_data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()

            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            if item.quantity <= 0:
                raise HTTPException(status_code=400, detail="Invalid quantity")

            if product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")

            total_price += product.price * item.quantity

            products_data.append({
                "product": product,
                "quantity": item.quantity
            })

        new_order = Order(
            user_id=current_user.id,
            total_price=total_price,
            status="pending"
        )

        db.add(new_order)
        db.flush()

        for data in products_data:
            product = data["product"]
            quantity = data["quantity"]

            product.stock -= quantity

            db.add(OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=quantity,
                price=product.price
            ))

        db.commit()
        db.refresh(new_order)

        return new_order

    except Exception:
        db.rollback()
        raise


# GET MY ORDERS (WITH STATUS FILTER)
@router.get("/", response_model=list[OrderResponse])
def get_my_orders(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Order).filter(Order.user_id == current_user.id)

    if status:
        query = query.filter(Order.status == status)

    return query.all()


# GET SINGLE ORDER
@router.get("/{order_id}", response_model=OrderResponse)
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
        raise HTTPException(status_code=404, detail="Order not found")

    return order


# DELETE ORDER
@router.delete("/{order_id}")
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
        raise HTTPException(status_code=404, detail="Order not found")

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity

    db.delete(order)
    db.commit()

    return {"message": "Order deleted successfully"}