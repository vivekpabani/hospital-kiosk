import requests
import datetime


def get_current_user_data(access_token):

    current_user_url = 'https://drchrono.com/api/users/current'

    response = requests.get(current_user_url, headers=get_headers(access_token))

    return response.json()

def get_doctor_appointments(access_token, doctor_id, adate=None):

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
            print("appointment", appointment)
            appointments.append(appointment)
        appointment_url = json['next']

    return appointments

def get_patient_details_by_id(access_token, patient_id):

    patients_url = 'https://drchrono.com/api/patients'
    patients_url = patients_url + '/' + str(patient_id) 

    response = requests.get(patients_url, headers=get_headers(access_token))
    result = response.json()

    return result

def update_patient_demographics(access_token, patient_id, doctor_id, data):

    patients_url = 'https://drchrono.com/api/patients'
    patients_url = patients_url + '/' + str(patient_id)

    data['doctor'] = '/api/doctors/' + str(doctor_id)

    response = requests.put(patients_url, data=data, headers=get_headers(access_token))

    return response.status_code in (200, 204)

def update_appointment_status(access_token, appointment_id, new_status):

    appointments_url = 'https://drchrono.com/api/appointments'
    appointment_url = appointments_url + '/' + str(appointment_id) 

    response = requests.get(appointment_url, headers=get_headers(access_token))
    appointment_data = response.json() 

    appointment_data['status'] = new_status

    response = requests.put(appointments_url, data=appointment_data, headers=get_headers(access_token))
    print('response', response)

    return response.status_code in (200, 204)

def get_headers(access_token):

    return {'Authorization': 'Bearer {0}'.format(access_token)}
