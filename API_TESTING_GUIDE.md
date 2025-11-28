# API Testing Guide

Complete guide to test all API endpoints with examples.

## Setup

1. Start the server: `python manage.py runserver`
2. Create a superuser: `python manage.py createsuperuser`
3. Use Swagger UI at: http://localhost:8000/swagger/

## Test Flow

### 1. User Registration
```bash
POST http://localhost:8000/api/auth/register/

{
    "username": "rehan_customer",
    "email": "rehan@example.com",
    "password": "Rehan@123",
    "password2": "Rehan@123",
    "phone": "9876543210",
    "role": "customer",
    "address": "123 Main Street",
    "city": "Mumbai",
    "state": "Maharashtra",
    "pincode": "400001"
}
```

### 2. Login
```bash
POST http://localhost:8000/api/auth/login/

{
    "email": "rehan@example.com",
    "password": "Rehan@123"
}

# Save the access token from response
```

### 3. Get Profile
```bash
GET http://localhost:8000/api/auth/profile/
Headers: Authorization: Bearer <your-access-token>
```

### 4. Create Category (Admin only)
```bash
POST http://localhost:8000/api/products/categories/
Headers: Authorization: Bearer <admin-token>

{
    "name": "Electronics",
    "description": "Electronic items and gadgets",
    "is_active": true
}
```

### 5. Create Product (Vendor/Admin)
First, create a vendor user or use admin account.

```bash
POST http://localhost:8000/api/products/create/
Headers: Authorization: Bearer <vendor-token>

{
    "name": "iPhone 15 Pro",
    "slug": "iphone-15-pro",
    "description": "Latest iPhone with A17 Pro chip",
    "category": 1,
    "price": "129999.00",
    "discount_price": "119999.00",
    "stock": 50,
    "is_available": true
}

# Note: Add image file in form-data
```

### 6. List Products
```bash
GET http://localhost:8000/api/products/

# With filters
GET http://localhost:8000/api/products/?category=1&ordering=-price
GET http://localhost:8000/api/products/?search=iphone
```

### 7. Get Product Details
```bash
GET http://localhost:8000/api/products/iphone-15-pro/
```

### 8. Create Review
```bash
POST http://localhost:8000/api/products/1/reviews/
Headers: Authorization: Bearer <user-token>

{
    "rating": 5,
    "comment": "Excellent product! Highly recommended."
}
```

### 9. Create Order
```bash
POST http://localhost:8000/api/orders/create/
Headers: Authorization: Bearer <user-token>

{
    "shipping_address": "123 Main Street, Apartment 4B",
    "shipping_city": "Mumbai",
    "shipping_state": "Maharashtra",
    "shipping_pincode": "400001",
    "phone": "9876543210",
    "payment_method": "cod",
    "items": [
        {
            "product": 1,
            "quantity": 2
        },
        {
            "product": 2,
            "quantity": 1
        }
    ]
}
```

### 10. List Orders
```bash
GET http://localhost:8000/api/orders/
Headers: Authorization: Bearer <user-token>

# Filter by status
GET http://localhost:8000/api/orders/?status=pending
```

### 11. Cancel Order
```bash
POST http://localhost:8000/api/orders/1/cancel/
Headers: Authorization: Bearer <user-token>
```

### 12. Admin - Update Order Status
```bash
PUT http://localhost:8000/api/orders/admin/1/update/
Headers: Authorization: Bearer <admin-token>

{
    "status": "shipped",
    "is_paid": true
}
```

### 13. Change Password
```bash
POST http://localhost:8000/api/auth/change-password/
Headers: Authorization: Bearer <user-token>

{
    "old_password": "Rehan@123",
    "new_password": "NewPass@123",
    "new_password2": "NewPass@123"
}
```

## Testing with Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(f"{BASE_URL}/api/auth/register/", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test@123",
    "password2": "Test@123",
    "role": "customer"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/api/auth/login/", json={
    "email": "test@example.com",
    "password": "Test@123"
})
tokens = response.json()
access_token = tokens['access']

# Get products
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(f"{BASE_URL}/api/products/", headers=headers)
print(response.json())
```

## Common Response Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded

## Rate Limiting Test

Try making more than 100 requests as anonymous user or 1000 as authenticated user to test throttling.

## Tips for Interview Demo

1. Start with Swagger UI - shows professionalism
2. Demonstrate user registration and login
3. Show JWT token usage
4. Create a product (shows CRUD)
5. Place an order (shows business logic)
6. Show filtering and search
7. Demonstrate role-based access (try accessing admin endpoint as customer)
8. Show error handling (invalid data, unauthorized access)

## Postman Collection

Import this JSON to Postman for quick testing:
1. Go to Swagger: http://localhost:8000/swagger.json
2. Copy the JSON
3. Import in Postman
4. Set up environment variables for tokens
