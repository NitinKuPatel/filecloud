from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django.conf import settings
from django.core.validators import FileExtensionValidator   

# Create your models here.
class CustomUser(AbstractUser):
    address = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    
class Files(models.Model):  # Class name should be PascalCase
    file_name = models.CharField(max_length=20)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="uploaded_files", on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/', max_length=264, null=True, validators=[FileExtensionValidator(['pdf'])])
    uploaded = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

class Images(models.Model):
    image_name = models.CharField(max_length=30)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="uploaded_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/', max_length=264, null=True, validators=[FileExtensionValidator(['jpg', 'png'])])
    uploaded = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image_name
