"""
Script to create sample data for testing and demo
Run: python manage.py shell < create_sample_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Category, Product
from orders.models import Order, OrderItem
from decimal import Decimal

User = get_user_model()

print("Creating sample data...")

# Create users
print("\n1. Creating users...")

# Admin user
admin, created = User.objects.get_or_create(
    email='admin@ecommerce.com',
    defaults={
        'username': 'admin',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
        'first_name': 'Admin',
        'last_name': 'User'
    }
)
if created:
    admin.set_password('Admin@123')
    admin.save()
    print("✓ Admin user created")

# Vendor user
vendor, created = User.objects.get_or_create(
    email='vendor@ecommerce.com',
    defaults={
        'username': 'vendor1',
        'role': 'vendor',
        'first_name': 'Vendor',
        'last_name': 'One',
        'phone': '9876543210',
        'city': 'Mumbai',
        'state': 'Maharashtra'
    }
)
if created:
    vendor.set_password('Vendor@123')
    vendor.save()
    print("✓ Vendor user created")

# Customer users
customer1, created = User.objects.get_or_create(
    email='customer1@example.com',
    defaults={
        'username': 'customer1',
        'role': 'customer',
        'first_name': 'Rahul',
        'last_name': 'Sharma',
        'phone': '9876543211',
        'address': '123 MG Road',
        'city': 'Bangalore',
        'state': 'Karnataka',
        'pincode': '560001'
    }
)
if created:
    customer1.set_password('Customer@123')
    customer1.save()
    print("✓ Customer 1 created")

customer2, created = User.objects.get_or_create(
    email='customer2@example.com',
    defaults={
        'username': 'customer2',
        'role': 'customer',
        'first_name': 'Priya',
        'last_name': 'Patel',
        'phone': '9876543212',
        'address': '456 Park Street',
        'city': 'Delhi',
        'state': 'Delhi',
        'pincode': '110001'
    }
)
if created:
    customer2.set_password('Customer@123')
    customer2.save()
    print("✓ Customer 2 created")

# Create categories
print("\n2. Creating categories...")

categories_data = [
    {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
    {'name': 'Clothing', 'description': 'Fashion and apparel'},
    {'name': 'Books', 'description': 'Books and educational materials'},
    {'name': 'Home & Kitchen', 'description': 'Home appliances and kitchen items'},
    {'name': 'Sports', 'description': 'Sports equipment and accessories'},
]

categories = []
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    categories.append(category)
    if created:
        print(f"✓ Category '{category.name}' created")

# Create products
print("\n3. Creating products...")

products_data = [
    {
        'name': 'iPhone 15 Pro',
        'slug': 'iphone-15-pro',
        'description': 'Latest iPhone with A17 Pro chip, titanium design, and advanced camera system',
        'category': categories[0],
        'price': Decimal('129999.00'),
        'discount_price': Decimal('119999.00'),
        'stock': 50,
    },
    {
        'name': 'Samsung Galaxy S24 Ultra',
        'slug': 'samsung-galaxy-s24-ultra',
        'description': 'Flagship Samsung phone with S Pen, 200MP camera, and AI features',
        'category': categories[0],
        'price': Decimal('124999.00'),
        'discount_price': Decimal('114999.00'),
        'stock': 45,
    },
    {
        'name': 'Sony WH-1000XM5',
        'slug': 'sony-wh-1000xm5',
        'description': 'Premium noise-cancelling wireless headphones',
        'category': categories[0],
        'price': Decimal('29990.00'),
        'discount_price': Decimal('26990.00'),
        'stock': 100,
    },
    {
        'name': 'MacBook Pro 14"',
        'slug': 'macbook-pro-14',
        'description': 'Apple MacBook Pro with M3 chip, 16GB RAM, 512GB SSD',
        'category': categories[0],
        'price': Decimal('199900.00'),
        'discount_price': None,
        'stock': 25,
    },
    {
        'name': 'Nike Air Max',
        'slug': 'nike-air-max',
        'description': 'Comfortable running shoes with air cushioning',
        'category': categories[4],
        'price': Decimal('8995.00'),
        'discount_price': Decimal('7495.00'),
        'stock': 150,
    },
    {
        'name': 'Levi\'s Denim Jacket',
        'slug': 'levis-denim-jacket',
        'description': 'Classic denim jacket, perfect for casual wear',
        'category': categories[1],
        'price': Decimal('4999.00'),
        'discount_price': Decimal('3999.00'),
        'stock': 80,
    },
    {
        'name': 'The Psychology of Money',
        'slug': 'psychology-of-money',
        'description': 'Bestselling book by Morgan Housel about wealth and happiness',
        'category': categories[2],
        'price': Decimal('399.00'),
        'discount_price': Decimal('299.00'),
        'stock': 200,
    },
    {
        'name': 'Instant Pot Duo',
        'slug': 'instant-pot-duo',
        'description': '7-in-1 electric pressure cooker',
        'category': categories[3],
        'price': Decimal('8999.00'),
        'discount_price': Decimal('7499.00'),
        'stock': 60,
    },
]

products = []
for prod_data in products_data:
    product, created = Product.objects.get_or_create(
        slug=prod_data['slug'],
        defaults={
            **prod_data,
            'vendor': vendor,
            'is_available': True
        }
    )
    products.append(product)
    if created:
        print(f"✓ Product '{product.name}' created")

# Create some reviews
print("\n4. Creating reviews...")

from products.models import Review

reviews_data = [
    {'product': products[0], 'user': customer1, 'rating': 5, 'comment': 'Excellent phone! Camera quality is amazing.'},
    {'product': products[0], 'user': customer2, 'rating': 4, 'comment': 'Great phone but a bit expensive.'},
    {'product': products[2], 'user': customer1, 'rating': 5, 'comment': 'Best headphones I have ever used!'},
    {'product': products[4], 'user': customer2, 'rating': 4, 'comment': 'Very comfortable for running.'},
]

for review_data in reviews_data:
    review, created = Review.objects.get_or_create(
        product=review_data['product'],
        user=review_data['user'],
        defaults={
            'rating': review_data['rating'],
            'comment': review_data['comment']
        }
    )
    if created:
        print(f"✓ Review created for {review.product.name}")

# Create sample orders
print("\n5. Creating sample orders...")

# Order 1
order1, created = Order.objects.get_or_create(
    order_number='ORD1234567890',
    defaults={
        'user': customer1,
        'shipping_address': '123 MG Road, Apartment 5B',
        'shipping_city': 'Bangalore',
        'shipping_state': 'Karnataka',
        'shipping_pincode': '560001',
        'phone': '9876543211',
        'status': 'delivered',
        'payment_method': 'online',
        'is_paid': True,
        'total_amount': Decimal('146989.00')
    }
)

if created:
    OrderItem.objects.create(
        order=order1,
        product=products[0],  # iPhone
        quantity=1,
        price=products[0].final_price
    )
    OrderItem.objects.create(
        order=order1,
        product=products[2],  # Headphones
        quantity=1,
        price=products[2].final_price
    )
    print("✓ Order 1 created (Delivered)")

# Order 2
order2, created = Order.objects.get_or_create(
    order_number='ORD0987654321',
    defaults={
        'user': customer2,
        'shipping_address': '456 Park Street, Floor 3',
        'shipping_city': 'Delhi',
        'shipping_state': 'Delhi',
        'shipping_pincode': '110001',
        'phone': '9876543212',
        'status': 'processing',
        'payment_method': 'cod',
        'is_paid': False,
        'total_amount': Decimal('7495.00')
    }
)

if created:
    OrderItem.objects.create(
        order=order2,
        product=products[4],  # Nike shoes
        quantity=1,
        price=products[4].final_price
    )
    print("✓ Order 2 created (Processing)")

print("\n" + "="*50)
print("Sample data creation completed!")
print("="*50)
print("\nLogin Credentials:")
print("\nAdmin:")
print("  Email: admin@ecommerce.com")
print("  Password: Admin@123")
print("\nVendor:")
print("  Email: vendor@ecommerce.com")
print("  Password: Vendor@123")
print("\nCustomer 1:")
print("  Email: customer1@example.com")
print("  Password: Customer@123")
print("\nCustomer 2:")
print("  Email: customer2@example.com")
print("  Password: Customer@123")
print("\n" + "="*50)
