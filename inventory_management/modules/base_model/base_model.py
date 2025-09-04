from django.db import models


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
