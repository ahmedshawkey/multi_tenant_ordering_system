import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User, Product, Order
from tenants.models import Tenant
from django.utils.timezone import now

# 🏢 Create Demo Tenant
tenant, _ = Tenant.objects.get_or_create(name='DemoCorp', defaults={'domain': 'democorp.test'})

# 👤 Create Demo Users with roles
users = [
    ('admin_user', 'admin'),
    ('operator_user', 'operator'),
    ('viewer_user', 'viewer'),
]

for username, role in users:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'role': role,
            'company': tenant,
            'email': f'{username}@democorp.test',
            'is_staff': True,
        }
    )
    if created:
        user.set_password('password123')
        user.save()

# 📦 Create Demo Products for Tenant
products = [
    ('Widget A', 49.99, 50),
    ('Gizmo B', 29.95, 30),
    ('Tool C', 99.99, 100),
]

for name, price, stock in products:
    Product.objects.get_or_create(
        name=name,
        company=tenant,
        defaults={
            'price': price,
            'stock': stock,
            'is_active': True,
            'created_by': user,
        }
    )

# 🧾 Create Demo Order
admin_user = User.objects.get(username='admin_user')
product = Product.objects.filter(company=tenant).first()

Order.objects.get_or_create(
    product=product,
    quantity=5,
    status='pending',
    shipped_at=None,
    company=tenant,
    created_by=admin_user,
    created_at=now()
)

print("✅ Demo data successfully seeded.")
