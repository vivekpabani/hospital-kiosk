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
            appointments.append(appointment)
        appointment_url = json['next']

    return appointments

def get_patient_details_by_id(access_token, patient_id):

    patients_url = 'https://drchrono.com/api/patients'
    patients_url = patients_url + '/' + str(patient_id) 

    response = requests.get(patients_url, headers=get_headers(access_token))
    result = response.json()

    patient_details = dict([('last_name', result['last_name']),
                    ('first_name', result['first_name']),
                    ('contact', result['cell_phone']),
                    ('address', result['address']),
                    ('email', result['email']),
                    ('ssn', result['social_security_number']),
                    ('id', result['id']),
                   ])

    return patient_details

def get_headers(access_token):

    return {'Authorization': 'Bearer {0}'.format(access_token)}
