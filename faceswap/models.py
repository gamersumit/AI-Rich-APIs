import uuid
from django.db import models

# Create your models here.
class FaceSwap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    source = models.URLField(null = True, blank = True)
    target = models.URLField(null = True, blank = True)
    swapped = models.URLField(null = True, blank = True)