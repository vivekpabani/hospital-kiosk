from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    """
    Model to store doctor's pin to access kiosk.
    """

    user = models.OneToOneField(User)
    pin = models.CharField(max_length=4)
