from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Boolean,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# =========================
# USER MODEL
# =========================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        index=True,
        nullable=True
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=True
    )

    hashed_password = Column(
        String,
        nullable=True
    )

    is_admin = Column(
        Boolean,
        default=False,
        nullable=True
    )

    password = Column(
        String,
        nullable=False,
        default=""
    )

    created_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=True
    )

    # User -> Orders
    orders = relationship(
        "Order",
        back_populates="user"
    )

    # User -> Cart
    cart = relationship(
        "Cart",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


# =========================
# PRODUCT MODEL
# =========================

class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    price = Column(
        Float,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    # Product -> OrderItems
    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )

    # Product -> CartItems
    cart_items = relationship(
        "CartItem",
        back_populates="product"
    )


# =========================
# CART MODEL
# =========================

class Cart(Base):
    __tablename__ = "carts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    # Cart -> User
    user = relationship(
        "User",
        back_populates="cart"
    )

    # Cart -> CartItems
    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )


# =========================
# CART ITEM MODEL
# =========================

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    cart_id = Column(
        Integer,
        ForeignKey("carts.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    # CartItem -> Cart
    cart = relationship(
        "Cart",
        back_populates="items"
    )

    # CartItem -> Product
    product = relationship(
        "Product",
        back_populates="cart_items"
    )


# =========================
# ORDER MODEL
# =========================

class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    total_price = Column(
        Float,
        nullable=False,
        default=0
    )

    status = Column(
        String,
        nullable=False,
        default="pending"
    )

    # Order -> User
    user = relationship(
        "User",
        back_populates="orders"
    )

    # Order -> OrderItems
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    # Order -> Payment
    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )


# =========================
# ORDER ITEM MODEL
# =========================

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    # OrderItem -> Order
    order = relationship(
        "Order",
        back_populates="items"
    )

    # OrderItem -> Product
    product = relationship(
        "Product",
        back_populates="order_items"
    )


# =========================
# PAYMENT MODEL
# =========================

class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="pending"
    )

    payment_method = Column(
        String,
        nullable=False
    )

    # Payment -> Order
    order = relationship(
        "Order",
        back_populates="payment"
    )

