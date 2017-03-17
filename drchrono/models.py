from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    """
    Model to store doctor's pin to access kiosk.
    """

    user = models.ForeignKey(User)
    pin = models.CharField(max_length=4, null=True, blank=True)


class Appointment(models.Model):
    """
    Model to represent the appointment instance.
    Data not stored on drchrono, and required to
    calculate time related measures are stored here.
    """

    status_choices = (('Confirmed', 'Confirmed'),
                      ('Arrived', 'Arrived'),
                      ('In Session', 'In Session'),
                      ('Complete', 'Complete'))

    appointment_id = models.CharField(max_length=30)
    patient_id = models.CharField(max_length=30)
    scheduled_time = models.DateField()
    arrival_time = models.DateField(null=True, blank=True)
    checkup_time = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_choices)
