from django.conf.urls import include, url
from django.contrib import admin

import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^set_kiosk_pin/$', views.set_kiosk_pin, name='set_kiosk_pin'),
    url(r'^kiosk/$', views.kiosk, name='kiosk'),
    url(r'^doctor_kiosk/$', views.doctor_kiosk, name='doctor_kiosk'),
    url(r'^validate_patient/$', views.validate_patient, name='validate_patient'),
    url(r'^validate_patient/(?P<appointment_id>[0-9]+)/', views.validate_patient, name='validate_patient'),
    url(r'^validate_doctor/$', views.validate_doctor, name='validate_doctor'),
    url(r'^update_demographics/$', views.update_demographics, name='update_demographics'),
    url(r'^update_demographics/(?P<appointment_id>[0-9]+)/', views.update_demographics, name='update_demographics'),
    url(r'^update_appointment_status/$', views.update_appointment_status, name='update_appointment_status'),
    url(r'^login_view/', views.login_view, name='login_view'),
    url(r'^logout_view/', views.logout_view, name='logout_view'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
