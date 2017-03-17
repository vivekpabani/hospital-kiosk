from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime

from .models import Doctor, Appointment
from .forms import (KioskPinForm,
                    PatientValidationForm,
                    DemographicsForm,
                    AppointmentStatusForm,
                    CheckInForm) 
from .utils import (get_current_user_data,
                    get_doctor_appointments,
                    update_patient_demographics,
                    update_appointment_status,
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

        scheduled_time = datetime.datetime.strptime(data['scheduled_time'], datetime_format)

        # Add appointment to database, if doesn't exist.
        try:
            appointment_instance = Appointment.objects.get(appointment_id=data['id'])
        except Appointment.DoesNotExist:
            appointment_instance = Appointment(appointment_id=data['id'],
                                               patient_id=data['patient'],
                                               scheduled_time=scheduled_time,
                                               status=data['status'])
            appointment_instance.save()

        # If status is Confirmed, add to list to display to user.
        if appointment_instance.status in ("", "Confirmed"):
            appointment = dict() 
            appointment['id'] = appointment_instance.appointment_id
            appointment['scheduled_time'] = appointment_instance.scheduled_time

            checkin_form = CheckInForm(initial={'appointment_id':appointment_instance.appointment_id,
                                            'patient_id':appointment_instance.patient_id})
                                   
            appointment['checkin_form'] = checkin_form

            appointments.append(appointment)

    context['appointments'] = appointments

    return render(request, 'kiosk.html', context)

def validate_patient(request, appointment_id=None):
    """
    Process validation form, and validate user.
    If validated, redirect to update_demographics
    If not validated, render kiosk.

    """

    access_token = request.user.social_auth.get(provider='drchrono').extra_data['access_token']

    if request.method == 'POST':

        patient_validation_form = PatientValidationForm(request.POST)

        if patient_validation_form.is_valid():

            data = patient_validation_form.cleaned_data

            first_name = data['first_name']
            last_name = data['last_name']
            appointment_id = data['appointment_id']
            appointments = Appointment.objects.filter(appointment_id=appointment_id)
            patient_id = appointments[0].patient_id

            patient_details = get_patient_details_by_id(access_token, patient_id)

            if patient_details['first_name'] == first_name and patient_details['last_name'] == last_name:
                request.session['validated_patient_appointment'] = str(appointment_id)
                update_demographics_redirect = '/update_demographics/' + str(appointment_id) + '/'
                return redirect(update_demographics_redirect)

            return redirect('/')

    elif appointment_id:

        appointments = Appointment.objects.filter(appointment_id=appointment_id)

        if not appointments:

            return redirect('/')

        patient_validation_form = PatientValidationForm(initial={'appointment_id':appointment_id})

        return render(request, 'patient_validation.html', {'patient_validation_form':patient_validation_form})


def update_demographics(request, appointment_id=None):
    """
    Update demographics of a patient with the form data in case of POST request.  
    Otherwise populate the form with patient's data and allow to update.
    """

    access_token = request.user.social_auth.get(provider='drchrono').extra_data['access_token']

    if request.method == 'POST':

        demographics_form = DemographicsForm(request.POST)

        if demographics_form.is_valid():

            data = demographics_form.cleaned_data

            request.session['validated_patient_appointment'] = ''

            demographics_updated = update_patient_demographics(access_token, data['patient_id'], data['doctor'], data)

            if demographics_updated or True:

                appointment_updated = update_appointment_status(access_token, appointment_id, "Arrived")

                appointment_instance = Appointment.objects.get(appointment_id=data['appointment_id'])
                appointment_instance.status = "Arrived"
                appointment_instance.arrival_time = datetime.datetime.now()
                appointment_instance.save()

            return redirect('/')

    elif appointment_id:

        appointments = Appointment.objects.filter(appointment_id=appointment_id)

        if not appointments:
            return redirect('/')

        if request.session.get('validated_patient_appointment', '') != str(appointment_id):
            return redirect('/')

        patient_id = appointments[0].patient_id
        
        patient_details = get_patient_details_by_id(access_token, patient_id)

        form_initial_values = {'first_name': patient_details['first_name'],
                               'last_name': patient_details['last_name'],
                               'gender': patient_details['gender'],
                               'appointment_id': appointment_id,
                               'patient_id': patient_details['id'],
                               'doctor': patient_details['doctor'],
                               'address': patient_details['address'],
                               'home_phone': patient_details['home_phone'],
                               'cell_phone': patient_details['cell_phone'],
                               'email': patient_details['email']
                               }

        demographics_form = DemographicsForm(initial = form_initial_values)
        return render(request, 'update_demographics.html', {'demographics_form':demographics_form})

    else:
        return redirect('/')

def doctor_kiosk(request):
    """
    Doctor's view of kiosk which gives him option to update status  
    and check the wait time of patients.
    """

    appointment_instances = Appointment.objects.filter(scheduled_time__contains=datetime.date.today())
    appointments = list()

    for appointment_instance in appointment_instances:

        appointment = {'scheduled_time': appointment_instance.scheduled_time,
                       'arrival_time': appointment_instance.arrival_time,
                       'status': appointment_instance.status,
                       'appointment_id': appointment_instance.appointment_id,
                       'patient_id': appointment_instance.patient_id}

        appointment_status_form = AppointmentStatusForm(initial={'status': appointment_instance.status,
                                                                 'appointment_id': appointment_instance.appointment_id})

        appointment['appointment_status_form'] = appointment_status_form
        appointments.append(appointment)

    context = {'appointments': appointments}

    return render(request, 'doctor_kiosk.html', context)

def update_appointment_status(request):
    """
    Update appointment status, and change timing accordingly.
    """
    print("update_appointment_status")
    if request.method == 'POST':
        appointment_status_form = AppointmentStatusForm(request.POST)
        if appointment_status_form.is_valid():
            print("valid form")
            data = appointment_status_form.cleaned_data
            appointment_id = data['appointment_id']
            status = data['status']
            print("appointment_id", appointment_id)
            try:
                appointment_instance = Appointment.objects.get(appointment_id=appointment_id)
            except Appointment.DoesNotExist:
                print("In Except") 
                return redirect('/doctor_kiosk/') 

            appointment_instance.update_status(status)

    return redirect('/doctor_kiosk/')    

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
