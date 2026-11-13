from django.db import models

class User(models.Model):
    username = models.CharField(max_length=500, unique=True)
    password_hash = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    display_name = models.CharField(max_length=500, default='USER')

    @classmethod
    def change_name(cls, username, display_name):
        try:
            user = cls.objects.get(username=username)
            user.display_name = display_name
            user.save(update_fields=["display_name"])
            return display_name 
        except cls.DoesNotExist:
            return 'USER'


    @classmethod
    def create_user(cls, username, password):
        if cls.objects.filter(username=username).exists():
            raise ValueError(f'пользователь с username {username} уже существует')
        return cls.objects.create(username=username, password_hash=password)


class Product(models.Model):
    name = models.CharField(max_length=64)
    descriptions = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Review(models.Model):
    author = models.CharField(max_length=64)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_comment(cls, author, comment):
        return cls.objects.create(author=author, text=comment)

