from django.db import models

# Create your models here.

class Profile(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image/')  #pip install pillow to ue image field
    gender = models.CharField(max_length=10,choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
