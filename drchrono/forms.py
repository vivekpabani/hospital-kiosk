from django import forms


class KioskPinForm(forms.Form):

    pin = forms.CharField(max_length=10, label="Enter Pin")
