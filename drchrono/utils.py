import requests
import datetime
from pytz import timezone

from .models import Appointment

def get_current_user_data(access_token):
    """
    Fetch current user data from server  
    """

    current_user_url = 'https://drchrono.com/api/users/current'

    response = requests.get(current_user_url, headers=get_headers(access_token))

    return response.json()

def get_doctor_appointments(access_token, doctor_id, adate=None):
    """
    Get doctor's today's appointments using doctor id. 
    """

    if adate and type(adate) == datetime.date:
        adate = adate.strftime('%Y-%m-%d')
    else:
        adate = datetime.date.today().strftime('%Y-%m-%d')

    appointment_url = 'https://drchrono.com/api/appointments'
    appointment_url = appointment_url + '?doctor=' + str(doctor_id) + '&date=' + str(adate)

    appointments = list()

    while appointment_url:

        response = requests.get(appointment_url, headers=get_headers(access_token))
        json = response.json()

        for appointment in json['results']:
            appointments.append(appointment)

        appointment_url = json['next']

    return appointments

def get_patient_details_by_id(access_token, patient_id):
    """
    Get patient's details from server.   
    """

    patients_url = 'https://drchrono.com/api/patients'
    patients_url = patients_url + '/' + str(patient_id) 

    response = requests.get(patients_url, headers=get_headers(access_token))
    result = response.json()

    return result

def update_patient_demographics(access_token, patient_id, doctor_id, data):
    """
    Modify patient demographics on server.
    """

    patients_url = 'https://drchrono.com/api/patients'
    patients_url = patients_url + '/' + str(patient_id)

    data['doctor'] = int(doctor_id)

    response = requests.put(patients_url, data=data, headers=get_headers(access_token))

    return response.status_code in (200, 204)

def update_appointment_on_server(access_token, appointment_id, new_status):
    """
    Modify appointment on server.
    """

    appointments_url = 'https://drchrono.com/api/appointments'
    appointments_url = appointments_url + '/' + str(appointment_id) 

    appointment_data = requests.get(appointments_url, headers=get_headers(access_token)).json()
    appointment_data['status'] = new_status

    response = requests.patch(appointments_url, data=appointment_data, headers=get_headers(access_token))

    return response.status_code in (200, 204)

def calculate_average_wait_time(doctor):
    """
    Calculate average wait time of all appointments of given doctor.
    """

    total_wait_time = 0
    appointments = Appointment.objects.filter(status__in=['Arrived','In Session','Complete'])
    tz = timezone('America/Los_Angeles')

    for appointment in appointments:

        if appointment.status == 'Arrived':
            total_wait_time += (datetime.datetime.now(tz) - appointment.arrival_time).total_seconds() / 60.0 
        elif appointment.status in ('Complete', 'In Session'):
            total_wait_time += (appointment.checkup_time - appointment.arrival_time).total_seconds() / 60.0

    return int(total_wait_time/len(appointments))

def sort_appointments(appointments):
    """
    Sort appointments based on status and scheduled_time 
    """

    status_rank = {"In Session": 1, "Arrived": 2, "Confirmed": 3, "Complete": 4}

    sorted_appointments = sorted(appointments, key=lambda a: (status_rank[a['status']], a['scheduled_time'])) 

    return sorted_appointments
    


def get_headers(access_token):
    """
    Get headers with accesss token
    """

    return {'Authorization': 'Bearer {0}'.format(access_token)}
