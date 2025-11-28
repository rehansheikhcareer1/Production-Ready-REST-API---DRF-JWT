# Quick Start Guide

Get the API running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation (Windows)

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
setup.bat
```

That's it! The script will:
- Create virtual environment
- Install dependencies
- Setup database
- Create superuser
- Load sample data

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Load sample data (optional)
python manage.py shell < create_sample_data.py

# 8. Start server
python manage.py runserver
```

## Installation (Linux/Mac)

```bash
# 1. Run setup script
chmod +x setup.sh
./setup.sh

# OR Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell < create_sample_data.py
python manage.py runserver
```

## Access the API

Once the server is running:

### 🌐 Main URLs

- **API Root**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Swagger Docs**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

### 🔑 Test Credentials

If you loaded sample data, use these credentials:

**Admin:**
- Email: `admin@ecommerce.com`
- Password: `Admin@123`

**Vendor:**
- Email: `vendor@ecommerce.com`
- Password: `Vendor@123`

**Customer:**
- Email: `customer1@example.com`
- Password: `Customer@123`

## Quick API Test

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"Test@123\",\"password2\":\"Test@123\",\"role\":\"customer\"}"
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"Test@123\"}"
```

Copy the `access` token from the response.

### 3. Get Products

```bash
curl -X GET http://localhost:8000/api/products/ ^
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Get Your Profile

```bash
curl -X GET http://localhost:8000/api/auth/profile/ ^
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Using Swagger UI (Easiest Way)

1. Open http://localhost:8000/swagger/
2. Click "Authorize" button (top right)
3. Login to get token:
   - Go to `/api/auth/login/`
   - Click "Try it out"
   - Enter credentials
   - Click "Execute"
   - Copy the `access` token
4. Paste token in Authorization dialog: `Bearer YOUR_TOKEN`
5. Now you can test all endpoints!

## Project Structure

```
ecommerce_api/
├── core/                      # Project settings
├── accounts/                  # User authentication
├── products/                  # Product management
├── orders/                    # Order management
├── media/                     # Uploaded files
├── manage.py                  # Django management
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
├── README.md                 # Full documentation
├── QUICKSTART.md             # This file
├── API_TESTING_GUIDE.md      # API testing examples
├── DEPLOYMENT_GUIDE.md       # Deployment instructions
├── INTERVIEW_GUIDE.md        # Interview preparation
└── FEATURES.md               # Complete features list
```

## Common Commands

```bash
# Start server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create sample data
python manage.py shell < create_sample_data.py

# Collect static files (for production)
python manage.py collectstatic

# Run Django shell
python manage.py shell
```

## Troubleshooting

### Port already in use
```bash
# Use different port
python manage.py runserver 8080
```

### Module not found
```bash
# Make sure virtual environment is activated
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Database errors
```bash
# Delete database and recreate
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Import errors
```bash
# Make sure you're in the correct directory
cd ecommerce_api

# Check Python version
python --version  # Should be 3.8+
```

## Next Steps

1. ✅ **Explore Swagger**: http://localhost:8000/swagger/
2. ✅ **Read API Testing Guide**: `API_TESTING_GUIDE.md`
3. ✅ **Check Features**: `FEATURES.md`
4. ✅ **Prepare for Interview**: `INTERVIEW_GUIDE.md`
5. ✅ **Deploy**: `DEPLOYMENT_GUIDE.md`

## Configuration

### Database (MySQL)

To use MySQL instead of SQLite, update `.env`:

```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
```

Then install MySQL client:
```bash
pip install mysqlclient
```

### Environment Variables

Edit `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite - default)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

## API Endpoints Overview

### Authentication
- `POST /api/auth/register/` - Register
- `POST /api/auth/login/` - Login
- `GET /api/auth/profile/` - Get profile
- `PUT /api/auth/profile/update/` - Update profile

### Products
- `GET /api/products/` - List products
- `POST /api/products/create/` - Create product
- `GET /api/products/{slug}/` - Product detail
- `PUT /api/products/{slug}/update/` - Update product

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/create/` - Create order
- `GET /api/orders/{id}/` - Order detail
- `POST /api/orders/{id}/cancel/` - Cancel order

### Categories
- `GET /api/products/categories/` - List categories
- `POST /api/products/categories/` - Create category

### Reviews
- `GET /api/products/{id}/reviews/` - List reviews
- `POST /api/products/{id}/reviews/` - Create review

## Support

For detailed documentation, check:
- `README.md` - Complete project documentation
- `API_TESTING_GUIDE.md` - How to test all endpoints
- `DEPLOYMENT_GUIDE.md` - How to deploy to production
- `INTERVIEW_GUIDE.md` - How to present in interviews

## Tips

1. **Use Swagger** for easy API testing
2. **Load sample data** to see the API in action
3. **Check admin panel** to see Django's built-in features
4. **Read the guides** for interview preparation
5. **Test all endpoints** before deploying

---

**You're all set! Start exploring the API! 🚀**

For questions or issues, check the documentation files or create an issue on GitHub.
