# 🛒 E-Commerce REST API

A production-ready e-commerce backend built with Django REST Framework, featuring JWT authentication, role-based access control, and comprehensive API documentation.

## ✨ What Makes This Special

This isn't just another CRUD API. I've built a complete e-commerce backend that handles real-world scenarios - from user authentication to order management. Every endpoint is secured, tested, and documented.

**Live Demo:** Try it out with the included HTML test interface 🚀

## 🎯 Key Features

### Authentication & Security
- JWT-based authentication (access + refresh tokens)
- Role-based permissions (Admin, Staff, Customer)
- Secure password handling with Django's built-in encryption
- Token refresh mechanism for seamless user experience

### Product Management
- Full CRUD operations for products
- Category-based organization
- Stock tracking and management
- Image upload support
- Price and discount handling

### Order System
- Complete order lifecycle management
- Order status tracking (Pending → Processing → Shipped → Delivered)
- Order history for customers
- Admin dashboard for order management

### User Accounts
- Custom user model with extended fields
- Profile management
- Registration and login endpoints
- Admin can manage all users

## 🛠️ Tech Stack

- **Framework:** Django 4.2 + Django REST Framework
- **Authentication:** Simple JWT
- **API Documentation:** drf-yasg (Swagger/OpenAPI)
- **Database:** SQLite (easily switchable to PostgreSQL/MySQL)
- **CORS:** django-cors-headers for frontend integration

## 📦 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/rehansheikhcareer1/Production-Ready-REST-API---DRF-JWT.git
cd Production-Ready-REST-API---DRF-JWT
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create admin user**
```bash
python create_admin.py
```

7. **Load sample data (optional)**
```bash
python create_sample_data.py
```

8. **Start the server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` 🎉

## 📚 API Documentation

Once the server is running, check out the interactive API docs:

- **Swagger UI:** `http://localhost:8000/swagger/`
- **ReDoc:** `http://localhost:8000/redoc/`

### Quick API Overview

#### Authentication
```
POST /api/accounts/register/     - Register new user
POST /api/accounts/login/        - Login and get tokens
POST /api/accounts/token/refresh/ - Refresh access token
GET  /api/accounts/profile/      - Get user profile
```

#### Products
```
GET    /api/products/           - List all products
POST   /api/products/           - Create product (Admin only)
GET    /api/products/{id}/      - Get product details
PUT    /api/products/{id}/      - Update product (Admin only)
DELETE /api/products/{id}/      - Delete product (Admin only)
```

#### Orders
```
GET    /api/orders/             - List user's orders
POST   /api/orders/             - Create new order
GET    /api/orders/{id}/        - Get order details
PATCH  /api/orders/{id}/        - Update order status (Admin only)
```

## 🔐 Authentication Flow

1. Register or login to get JWT tokens
2. Use access token in Authorization header: `Bearer <token>`
3. Access token expires in 60 minutes
4. Refresh token expires in 1 day
5. Use refresh endpoint to get new access token

## 👥 User Roles

- **Customer:** Can browse products, place orders, view own orders
- **Staff:** Can manage products and view all orders
- **Admin:** Full access to all endpoints and admin panel

## 🧪 Testing

Use the included `test_api.html` file to test all endpoints without writing code. Just open it in your browser!

## 📁 Project Structure

```
ecommerce_api/
├── accounts/          # User management & authentication
├── products/          # Product catalog
├── orders/            # Order processing
├── core/              # Project settings
├── manage.py
├── requirements.txt
└── README.md
```

## 🚀 Deployment Ready

This project is configured for easy deployment:

- Environment variables for sensitive data
- CORS configured for frontend integration
- Static files handling
- Database-agnostic (switch to PostgreSQL in production)
- Comprehensive error handling

## 💡 What I Learned

Building this project taught me:
- Designing RESTful APIs following best practices
- Implementing secure authentication systems
- Managing complex relationships in Django ORM
- Writing clean, maintainable code
- API documentation and testing

## 🤝 Connect With Me

Found this interesting? Let's connect!

- **GitHub:** [@rehansheikhcareer1](https://github.com/rehansheikhcareer1)
- **LinkedIn:** [Add your LinkedIn]
- **Email:** [Add your email]

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ If you found this project helpful, please give it a star!

**Note:** This is a portfolio project demonstrating my backend development skills. Feel free to use it as a reference or starting point for your own projects.
