import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    profile_id = models.CharField(max_length=100, default='0')
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class EmailConfirmation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    user = models.ForeignKey(CustomUser, related_name='email_confirmation', on_delete=models.CASCADE)
    code = models.PositiveSmallIntegerField(max_length=6)

