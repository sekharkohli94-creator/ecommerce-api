from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, List


# =========================
# USER SCHEMAS
# =========================

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)


class UserResponse(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


# =========================
# PRODUCT SCHEMAS
# =========================

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# ORDER SCHEMAS
# =========================

class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


# =========================
# PAYMENT SCHEMAS
# =========================

class PaymentCreate(BaseModel):
    order_id: int = Field(gt=0)
    payment_method: str = Field(min_length=2, max_length=30)


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    status: str
    payment_method: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# ORDER STATUS
# =========================

class OrderStatusUpdate(BaseModel):
    status: str = Field(min_length=2, max_length=30)


# =========================
# PAYMENT STATUS
# =========================

class PaymentStatusUpdate(BaseModel):
    status: str = Field(min_length=2, max_length=30)


# =========================
# CART SCHEMAS
# =========================

class CartItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)