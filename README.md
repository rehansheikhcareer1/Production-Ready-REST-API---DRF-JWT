# 🛒 E-Commerce REST API

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14.0-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Production-ready REST API for E-Commerce platform built with Django REST Framework, featuring JWT authentication, role-based access control, and comprehensive CRUD operations.

**Live Demo:** [Coming Soon]  
**Developer:** Rehan - Full Stack Python Developer

## 🚀 Features

- **User Authentication & Authorization**
  - JWT token-based authentication
  - Session authentication support
  - Role-based access (Admin, Vendor, Customer)
  - User registration and profile management
  - Password change functionality

- **Product Management**
  - Complete CRUD operations for products
  - Category management
  - Product images and gallery
  - Product reviews and ratings
  - Search, filter, and pagination
  - Stock management

- **Order Management**
  - Create and track orders
  - Order status management
  - Multiple payment methods
  - Order history
  - Admin order management

- **API Features**
  - Swagger/OpenAPI documentation
  - Rate limiting (throttling)
  - CORS support
  - Comprehensive error handling
  - Input validation
  - Pagination on all list endpoints

## 📋 Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)
- MySQL (optional, SQLite by default)

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd ecommerce_api
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# For SQLite (default)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# For MySQL (uncomment and configure)
# DB_ENGINE=django.db.backends.mysql
# DB_NAME=ecommerce_db
# DB_USER=root
# DB_PASSWORD=yourpassword
# DB_HOST=localhost
# DB_PORT=3306
```

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run development server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **JSON Schema**: http://localhost:8000/swagger.json

## 🔑 API Endpoints

### Authentication
```
POST   /api/auth/register/          - Register new user
POST   /api/auth/login/             - Login (get JWT tokens)
POST   /api/auth/token/refresh/     - Refresh access token
GET    /api/auth/profile/           - Get current user profile
PUT    /api/auth/profile/update/    - Update user profile
POST   /api/auth/change-password/   - Change password
```

### Users (Admin only)
```
GET    /api/auth/users/             - List all users
GET    /api/auth/users/{id}/        - Get user details
PUT    /api/auth/users/{id}/        - Update user
DELETE /api/auth/users/{id}/        - Delete user
```

### Categories
```
GET    /api/products/categories/           - List categories
POST   /api/products/categories/           - Create category (Admin)
GET    /api/products/categories/{id}/      - Get category details
PUT    /api/products/categories/{id}/      - Update category (Admin)
DELETE /api/products/categories/{id}/      - Delete category (Admin)
```

### Products
```
GET    /api/products/                      - List all products
POST   /api/products/create/               - Create product (Vendor/Admin)
GET    /api/products/my-products/          - List vendor's products
GET    /api/products/{slug}/               - Get product details
PUT    /api/products/{slug}/update/        - Update product
DELETE /api/products/{slug}/delete/        - Delete product
```

### Reviews
```
GET    /api/products/{id}/reviews/         - List product reviews
POST   /api/products/{id}/reviews/         - Create review
GET    /api/products/reviews/{id}/         - Get review details
PUT    /api/products/reviews/{id}/         - Update review
DELETE /api/products/reviews/{id}/         - Delete review
```

### Orders
```
GET    /api/orders/                        - List user's orders
POST   /api/orders/create/                 - Create new order
GET    /api/orders/{id}/                   - Get order details
POST   /api/orders/{id}/cancel/            - Cancel order
GET    /api/orders/admin/all/              - List all orders (Admin)
PUT    /api/orders/admin/{id}/update/      - Update order status (Admin)
```

## 🔐 Authentication

This API uses JWT (JSON Web Tokens) for authentication.

### Getting Tokens
```bash
POST /api/auth/login/
{
    "email": "user@example.com",
    "password": "password123"
}
```

Response:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using Tokens
Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Refreshing Tokens
```bash
POST /api/auth/token/refresh/
{
    "refresh": "your-refresh-token"
}
```

## 👥 User Roles

1. **Customer** (default)
   - Browse products
   - Create orders
   - Write reviews
   - Manage own profile

2. **Vendor**
   - All customer permissions
   - Create and manage products
   - View product analytics

3. **Admin**
   - Full system access
   - User management
   - Category management
   - Order management
   - All CRUD operations

## 🔍 Filtering & Search

### Products
```bash
# Search by name or description
GET /api/products/?search=laptop

# Filter by category
GET /api/products/?category=1

# Filter by vendor
GET /api/products/?vendor=2

# Order by price
GET /api/products/?ordering=price

# Combine filters
GET /api/products/?category=1&ordering=-created_at&search=phone
```

### Orders
```bash
# Filter by status
GET /api/orders/?status=pending

# Filter by payment method
GET /api/orders/?payment_method=cod

# Search by order number
GET /api/orders/admin/all/?search=ORD123
```

## 📊 Rate Limiting

API implements rate limiting to prevent abuse:

- **Anonymous users**: 100 requests per day
- **Authenticated users**: 1000 requests per day

## 🧪 Testing the API

### Using cURL
```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test@123",
    "password2": "Test@123",
    "role": "customer"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test@123"
  }'

# Get products (with token)
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer <your-access-token>"
```

### Using Postman
1. Import the API collection from Swagger JSON
2. Set up environment variables for tokens
3. Test all endpoints interactively

## 🚀 Deployment

### Render.com
1. Create new Web Service
2. Connect your repository
3. Set environment variables
4. Deploy

### PythonAnywhere
1. Upload code to PythonAnywhere
2. Create virtual environment
3. Configure WSGI file
4. Set up static files
5. Reload web app

### Environment Variables for Production
```env
SECRET_KEY=<strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.mysql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306
```

## 📁 Project Structure
```
ecommerce_api/
├── core/                   # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # User authentication
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── permissions.py
├── products/               # Product management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── admin.py
├── orders/                 # Order management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── admin.py
├── media/                  # Uploaded files
├── manage.py
└── requirements.txt
```

## 🛡️ Security Features

- Password hashing with Django's built-in system
- JWT token authentication
- CORS configuration
- CSRF protection
- SQL injection prevention (Django ORM)
- XSS protection
- Rate limiting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Developer

Developed by Rehan - Full Stack Python Developer

## 📧 Contact

For any queries or support, please contact: [your-email@example.com]

---

**Note**: This is a portfolio project demonstrating production-ready REST API development with Django REST Framework.
