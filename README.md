# 🛒 E-Commerce Backend API

A production-style RESTful E-Commerce Backend API built with **Python, FastAPI, PostgreSQL, SQLAlchemy, Pydantic, JWT Authentication, and Alembic**.

This project provides a complete backend system for an e-commerce application, including user authentication, product management, shopping cart, stock management, checkout, orders, payments, and admin management.

---

## 🌐 Live Demo

**Live API:**  
https://ecommerce-api-pagd.onrender.com

**Swagger Documentation:**  
https://ecommerce-api-pagd.onrender.com/docs

**ReDoc Documentation:**  
https://ecommerce-api-pagd.onrender.com/redoc

---

## 🚀 Features

### 🔐 Authentication

- User registration
- User login
- JWT-based authentication
- Password hashing with bcrypt
- Current user profile
- Protected API endpoints
- Role-based admin authorization

### 📦 Products

- Create products
- Get all products
- Get product by ID
- Update products
- Delete products
- Product search
- Stock management
- Stock validation

### 🛒 Shopping Cart

- Add products to cart
- View cart
- Update cart quantity
- Remove products from cart
- Automatic stock validation
- Prevent adding more products than available stock

### 📋 Orders

- Create orders
- View order history
- View individual orders
- Checkout cart
- Automatic stock reduction
- Order status management
- Order-item management

### 💳 Payments

- Create payment records
- View payment details
- Update payment status
- Link payments with orders

> Payment records are implemented as backend payment management. No external payment gateway is currently integrated.

### 👨‍💼 Admin

- Admin authorization
- Create and manage products
- View all users
- View individual users
- View all orders
- View individual orders
- Update order status

### 🗄️ Database

- PostgreSQL
- SQLAlchemy ORM
- Relational database design
- Foreign-key relationships
- Alembic database migrations

### 📚 API Documentation

- Swagger UI
- ReDoc
- OpenAPI documentation
- Interactive API testing

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Backend web framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM |
| Pydantic | Data validation |
| JWT | Authentication |
| Passlib / bcrypt | Password hashing |
| Alembic | Database migrations |
| Uvicorn | ASGI server |
| Render | Deployment |

---

## 🏗️ Architecture

The project follows a modular backend architecture.

```text
Client
  │
  ▼
FastAPI
  │
  ├── Authentication
  │      ├── Register
  │      ├── Login
  │      └── JWT
  │
  ├── Products
  │
  ├── Cart
  │
  ├── Orders
  │
  ├── Payments
  │
  └── Admin
         │
         ▼
     SQLAlchemy ORM
         │
         ▼
     PostgreSQL