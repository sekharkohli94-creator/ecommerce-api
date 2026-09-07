# 🛒 E-Commerce Backend API

A RESTful E-Commerce Backend API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Pydantic**, **JWT Authentication**, and **Alembic**.

This project provides a complete backend system for an e-commerce application, including authentication, products, shopping cart, orders, checkout, payments, and admin management.

---

## 🚀 Features

### 🔐 Authentication

- User registration
- User login
- JWT-based authentication
- Password hashing with bcrypt
- Current user profile
- Admin authorization
- Protected API endpoints

### 📦 Products

- Create products
- Get all products
- Get product by ID
- Update products
- Delete products
- Product search
- Stock management

### 🛒 Shopping Cart

- Add products to cart
- View cart
- Update cart quantity
- Remove products from cart
- Stock validation

### 📋 Orders

- Create orders
- View order history
- View individual orders
- Checkout cart
- Automatic stock reduction
- Order status management

### 💳 Payments

- Create payment records
- View payment details
- Update payment status
- Link payments with orders

### 👨‍💼 Admin

- Admin authentication
- Manage products
- View all users
- View individual users
- View all orders
- View individual orders
- Update order status

### 🗄️ Database

- PostgreSQL
- SQLAlchemy ORM
- Alembic database migrations
- Relational database design

### 📚 API Documentation

- Swagger UI
- ReDoc
- OpenAPI documentation

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Backend framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Pydantic | Data validation |
| JWT | Authentication |
| Passlib / bcrypt | Password hashing |
| Alembic | Database migrations |
| Uvicorn | ASGI server |

---

## 📁 Project Structure

```text
ecommerce-api/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── products.py
│       ├── cart.py
│       ├── orders.py
│       ├── payments.py
│       ├── admin_products.py
│       ├── admin_orders.py
│       └── admin_users.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── alembic.ini
├── create_tables.py
├── requirements.txt
├── README.md
└── .gitignore

git clone https://github.com/sekharkohli94-creator/ecommerce-api.git