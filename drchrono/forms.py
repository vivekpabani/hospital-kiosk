from django import forms
from .models import Appointment


class KioskPinForm(forms.Form):

    pin = forms.CharField(max_length=10, label="Enter Pin", widget=forms.PasswordInput)

class DoctorValidationForm(forms.Form):

    pin = forms.CharField(max_length=10, label="Enter Pin", widget=forms.PasswordInput)

class CheckInForm(forms.Form):

    appointment_id = forms.CharField(required=True, widget=forms.HiddenInput())
    patient_id = forms.CharField(required=True, widget=forms.HiddenInput())

class PatientValidationForm(forms.Form):

    first_name = forms.CharField(required=True, max_length=50, label="First Name")
    last_name = forms.CharField(required=True, max_length=50, label="Last Name")
    appointment_id = forms.CharField(required=True, widget=forms.HiddenInput())

class DemographicsForm(forms.Form):

    patient_id = forms.CharField(required=False, widget=forms.HiddenInput())
    doctor = forms.CharField(required=False, widget=forms.HiddenInput())
    appointment_id = forms.CharField(required=False, widget=forms.HiddenInput())

    # make these read-only.
    first_name = forms.CharField(max_length=50, label="First Name", widget=forms.TextInput(attrs={'readonly':'readonly'}))
    last_name = forms.CharField(max_length=50, label="Last Name", widget=forms.TextInput(attrs={'readonly':'readonly'}))
    gender = forms.CharField(widget=forms.Select(choices=(('Male', 'Male'),('Female', 'Female'),('Other', 'Other'))))

    address = forms.CharField(max_length=200, required=False, widget=forms.Textarea)
    home_phone = forms.CharField(max_length=12, required=False)
    cell_phone = forms.CharField(max_length=12, required=False)
    email = forms.EmailField(required=False)

class AppointmentStatusForm(forms.Form):

    appointment_id = forms.CharField(required=False, widget=forms.HiddenInput())
    status = forms.CharField(required=False, label='', widget=forms.Select(choices=Appointment.status_choices, attrs={"onChange":"form.submit()"}))
