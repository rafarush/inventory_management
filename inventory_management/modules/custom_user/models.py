import uuid

from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number1 = models.CharField(max_length=15)
    phone_number2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100)
    is_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return self.username


