from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(AbstractUser):
    where_active = models.BooleanField(default=False)

    