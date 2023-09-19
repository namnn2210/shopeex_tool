from django.db import models
from django.utils import timezone
from users.models import CustomUser

# Create your models here.
class ProcessData(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Add a ForeignKey to User model
    cookie = models.TextField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.IntegerField(default=-1)
    note = models.TextField(default='')
    created_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=7))