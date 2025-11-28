#!/bin/bash

echo "========================================"
echo "E-Commerce API Setup Script"
echo "========================================"
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
echo "Virtual environment created!"
echo ""

echo "Step 2: Activating virtual environment..."
source venv/bin/activate
echo ""

echo "Step 3: Installing dependencies..."
pip install -r requirements.txt
echo "Dependencies installed!"
echo ""

echo "Step 4: Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created! Please update it with your settings."
else
    echo ".env file already exists."
fi
echo ""

echo "Step 5: Running migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Database setup complete!"
echo ""

echo "Step 6: Creating superuser..."
echo "Please enter superuser details:"
python manage.py createsuperuser
echo ""

echo "Step 7: Loading sample data..."
python manage.py shell < create_sample_data.py
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the server, run:"
echo "  python manage.py runserver"
echo ""
echo "Then visit:"
echo "  - API: http://localhost:8000/"
echo "  - Admin: http://localhost:8000/admin/"
echo "  - Swagger: http://localhost:8000/swagger/"
echo ""
echo "========================================"
