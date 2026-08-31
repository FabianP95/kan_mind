"""User profile model used for authentication and display metadata."""

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
