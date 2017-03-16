from django import forms


class KioskPinForm(forms.Form):

    pin = forms.CharField(max_length=10, label="Enter Pin")


class CheckInForm(forms.Form):

    appointment_id = forms.CharField(required=True, widget=forms.HiddenInput())
    patient_id = forms.CharField(required=True, widget=forms.HiddenInput())
