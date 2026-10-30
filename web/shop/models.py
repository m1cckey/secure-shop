from django.db import models

class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    password_hash = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    name = models.CharField(max_length=64)
    descriptions = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)