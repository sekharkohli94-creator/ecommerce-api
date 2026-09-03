from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user,get_current_admin 
from app.models import Payment, Order
from app.schemas import PaymentCreate, PaymentResponse



router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# =========================================================
# CREATE NORMAL PAYMENT
# =========================================================

@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
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
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Payment can only be created for a pending order"
        )

    existing_payment = db.query(Payment).filter(
        Payment.order_id == order.id
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail="Payment already exists"
        )

    allowed_methods = [
        "UPI",
        "card",
        "netbanking",
        "cod"
    ]

    if payment_data.payment_method.lower() not in [
        method.lower() for method in allowed_methods
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment method"
        )

    new_payment = Payment(
        order_id=order.id,
        amount=order.total_price,
        payment_method=payment_data.payment_method,
        status="pending"
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment



    
      

# =========================================================
# ADMIN GET PAYMENTS WITH FILTER + PAGINATION
# =========================================================

@router.get(
    "/admin/all",
    response_model=list[PaymentResponse]
)
def get_all_payments(
    payment_status: str = None,
    payment_method: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be greater than 0"
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )

    query = db.query(Payment)

    if payment_status:
        query = query.filter(
            Payment.status == payment_status
        )

    if payment_method:
        query = query.filter(
            Payment.payment_method == payment_method
        )

    skip = (page - 1) * limit

    payments = query.offset(skip).limit(limit).all()

    return payments

# =========================================================
# GET MY PAYMENT
# =========================================================

@router.get(
    "/{payment_id}",
    response_model=PaymentResponse
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    order = db.query(Order).filter(
        Order.id == payment.order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return payment



# =========================================================
# ADMIN UPDATE PAYMENT STATUS
# =========================================================

@router.put(
    "/{payment_id}/status",
    response_model=PaymentResponse
)
def update_payment_status(
    payment_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    allowed_statuses = [
        "pending",
        "completed",
        "failed"
    ]

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment status"
        )

    if payment.status == "completed":
        raise HTTPException(
            status_code=400,
            detail="Payment is already completed"
        )

    payment.status = status

    order = db.query(Order).filter(
        Order.id == payment.order_id
    ).first()

    if order:
        if status == "completed":
            order.status = "confirmed"

        elif status == "failed":
            order.status = "cancelled"

    db.commit()
    db.refresh(payment)

    return payment