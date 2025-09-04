import uuid
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from djangoProject import settings
from inventory_management.modules.base_model.base_model import BaseModel


class CustomUser(AbstractUser, BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number1 = models.CharField(max_length=15)
    phone_number2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100)
    is_confirmed = models.BooleanField(default=False)

    def send_email(self, subject, template_name, context, from_email=settings.EMAIL_HOST_USER):
        to_email = self.email
        text_content = "Este correo requiere soporte para HTML."
        html_content = render_to_string(template_name, context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def __str__(self):
        return self.username
