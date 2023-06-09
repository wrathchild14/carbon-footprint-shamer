from django.db import models

# Create your models here.
from django.db import models


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')


class CarbonData(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='None')
    message = models.TextField(default='')
    damages = models.TextField(default='')
    carbon = models.DecimalField(max_digits=10, decimal_places=2)
    distance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_path = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.name
