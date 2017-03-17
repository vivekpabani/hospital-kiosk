from django import forms


class KioskPinForm(forms.Form):

    pin = forms.CharField(max_length=10, label="Enter Pin")


class CheckInForm(forms.Form):

    appointment_id = forms.CharField(required=True, widget=forms.HiddenInput())
    patient_id = forms.CharField(required=True, widget=forms.HiddenInput())

class PatientValidationForm(forms.Form):

    first_name = forms.CharField(required=True, max_length=50, label="First Name")
    last_name = forms.CharField(required=True, max_length=50, label="Last Name")
    patient_id = forms.CharField(required=True, widget=forms.HiddenInput())
