from django.db import models
from django.contrib.auth.models import User
import datetime

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
    scheduled_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True, blank=True)
    checkup_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_choices)

    def update_status(self, new_status):
        """
        Update appointment status, and change timing accordingly.
        """
        self.status = new_status

        current_time = datetime.datetime.now()
        if new_status == "Confirmed":
            self.arrival_time = None
            self.checkup_time = None
        if new_status == "Arrived":
            self.arrival_time = current_time
            self.checkup_time = None
        elif new_status == "In Session":
            self.checkup_time = current_time
            if not self.arrival_time:
                self.arrival_time = current_time

        self.save()
