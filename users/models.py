from django.db import models
from django.contrib.auth.models import AbstractUser

from main.models import Branch


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

