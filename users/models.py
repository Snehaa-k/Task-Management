# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    admin = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_users')

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
