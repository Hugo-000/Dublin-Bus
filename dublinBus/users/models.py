from django.db import models
from django.contrib.auth.models import User

class Addresses(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    addresses = models.JSONField()