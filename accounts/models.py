from django.contrib.auth.models import AbstractUser
from django.db import models
from tenants.models import Tenant  # your Company model

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
