from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add custom fields here
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    
