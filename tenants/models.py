from django.db import models

# Create your models here.


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name