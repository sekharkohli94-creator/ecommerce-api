from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, get_current_admin
from app.models import Payment, Order
from app.schemas import PaymentCreate, PaymentResponse

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

# CREATE PAYMENT
@router.post("/", response_model=PaymentResponse)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.id == payment_data.order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    existing = db.query(Payment).filter(Payment.order_id == order.id).first()

    if existing:
        raise HTTPException(status_code=400, detail="Payment already exists")

    payment = Payment(
        order_id=order.id,
        amount=order.total_price,
        payment_method=payment_data.payment_method,
        status="pending"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


# UPDATE PAYMENT STATUS (ADMIN)
@router.put("/{payment_id}/status", response_model=PaymentResponse)
def update_payment_status(
    payment_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    allowed_statuses = ["pending", "completed", "failed"]

    if status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    payment.status = status

    if status == "completed":
        payment.order.status = "confirmed"
    elif status == "failed":
        payment.order.status = "cancelled"

    db.commit()
    db.refresh(payment)

    return payment