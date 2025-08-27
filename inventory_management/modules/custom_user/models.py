from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models


class CustomUser(AbstractUser):
    id_number = models.CharField(max_length=11, unique=True)
    passport_number = models.CharField(max_length=15, unique=True)
    license_number = models.CharField(max_length=15, unique=True)
    phone_number1 = models.CharField(max_length=15)
    phone_number2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100)


    def __str__(self):
        return self.username


