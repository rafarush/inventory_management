from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class BaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    class Meta:
        abstract = True
