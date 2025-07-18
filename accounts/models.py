from django.contrib.auth.models import AbstractUser
from django.db import models
from tenants.models import Tenant  # Company model
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('operator', 'Operator'),
        ('viewer', 'Viewer'),
    ]

    company = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name='users'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def is_operator(self):
        return self.role == 'operator'

    def is_viewer(self):
        return self.role == 'viewer'


class CompanyScopedModel(models.Model):
    company = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="%(class)s_items"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Product(CompanyScopedModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    last_updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # for soft deletion

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class Order(CompanyScopedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    shipped_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} x {self.quantity} ({self.status})"
