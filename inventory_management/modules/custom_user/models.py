import uuid
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from djangoProject import settings


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number1 = models.CharField(max_length=15)
    phone_number2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100)
    is_confirmed = models.BooleanField(default=False)

    def send_email(self, subject, template_name, context, from_email=settings.EMAIL_HOST_USER):
        """
        Envía un correo estilizado en HTML usando EmailMultiAlternatives.
        :param subject: Asunto del correo
        :param template_name: Ruta al template HTML para el cuerpo del email
        :param context: Contexto para renderizar el template
        :param from_email: Correo remitente, si no se especifica se usará default
        """
        to_email = self.email
        text_content = "Este correo requiere soporte para HTML."  # Texto plano alternativo
        html_content = render_to_string(template_name, context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def __str__(self):
        return self.username
