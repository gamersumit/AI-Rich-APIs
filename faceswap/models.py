import uuid
from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.
class FaceSwap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    source = CloudinaryField('image', null = True, blank = True)
    target = CloudinaryField('image', null = True, blank = True)
    swapped = CloudinaryField('image', null = True, blank = True)