import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create admin user
if not User.objects.filter(email='admin@example.com').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        role='admin'
    )
    print("✅ Admin user created!")
    print("Email: admin@example.com")
    print("Password: admin123")
else:
    # Update existing admin password
    admin = User.objects.get(email='admin@example.com')
    admin.set_password('admin123')
    admin.is_superuser = True
    admin.is_staff = True
    admin.role = 'admin'
    admin.save()
    print("✅ Admin user updated!")
    print("Email: admin@example.com")
    print("Password: admin123")
