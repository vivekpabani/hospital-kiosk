from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime

from .models import Doctor, Appointment
from .forms import (KioskPinForm,
                    CheckInForm) 
from .utils import (get_current_user_data,
                    get_doctor_appointments,
                    get_patient_details_by_id)

@login_required
def home(request):
    """
    home view where user-doctor lands after authorizing with drchrono.
    if it is first visit of doctor, then redirect to kiosk pin set up,
    otherwise redirect to kiosk.
    """

    access_token = request.user.social_auth.get(provider='drchrono').extra_data['access_token']

    # if doctor's first time on kiosk, ask to set up pin. 
    doctor = Doctor.objects.filter(user=request.user)
    if not doctor or doctor[0].pin == Doctor._meta.get_field('pin').get_default():
        return redirect('set_kiosk_pin/')

    request.session['kiosk_pin_set'] = True
    return redirect('kiosk/')

def set_kiosk_pin(request):
    """
    process kiosk pin form, and set up if valid pin.
    redirect to home if setup successfully.
    """    

    if request.method == 'POST':
        kiosk_pin_form = KioskPinForm(request.POST)
        if kiosk_pin_form.is_valid():
            data = kiosk_pin_form.cleaned_data
            pin = data['pin']

            doctor = Doctor(user=request.user, pin=pin) 
            doctor.save()

            return redirect('/') 

    else:
        kiosk_pin_form = KioskPinForm()
        return render(request, 'kiosk_pin.html', {'kiosk_pin_form':kiosk_pin_form})


def kiosk(request):
    """
    Display today's appointments with option to check in.
    Also provide option to toggle between doctor's kiosk.
    """

    access_token = request.user.social_auth.get(provider='drchrono').extra_data['access_token']

    # fetch current user information
    current_user = get_current_user_data(access_token) 
    doctor_id = current_user['id'] 

    # fetch today's appointments of current user
    appointments_data = get_doctor_appointments(access_token, doctor_id) 

    context = dict()
    appointments = list()

    datetime_format = '%Y-%m-%dT%H:%M:%S'

    for data in appointments_data:
        appointment_id = data['id']
        scheduled_time = datetime.strptime(data['scheduled_time'], datetime_format)
        status = data['status']
        patient_id = data['patient']

        # Add appointment to database, if doesn't exist.
        if not Appointment.objects.filter(appointment_id=data['id']):
            appointment_instance = Appointment(appointment_id=appointment_id,
                                               scheduled_time=scheduled_time,
                                               status=status)

            appointment_instance.save()

        # Add to list to display to user.
        appointment = dict() 
        appointment['id'] = appointment_id
        appointment['scheduled_time'] = scheduled_time

        checkin_form = CheckInForm(initial={'appointment_id':appointment_id,
                                            'patient_id':patient_id})
                                   
        appointment['checkin_form'] = checkin_form

        appointments.append(appointment)

    context['appointments'] = appointments

    return render(request, 'kiosk.html', context)

def login_view(request):
    """
    render login page
    """

    return render(request, 'login.html')

@login_required
def logout_view(request):
    """
    logout and render login page again
    """

    auth_logout(request)

    return redirect('/')
