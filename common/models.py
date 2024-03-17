from django.db import models
import uuid


class BaseModelWithUID(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True