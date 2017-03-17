from django.conf.urls import include, url
from django.contrib import admin

import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^set_kiosk_pin/', views.set_kiosk_pin, name='set_kiosk_pin'),
    url(r'^kiosk/', views.kiosk, name='kiosk'),
    url(r'^validate_patient/$', views.validate_patient, name='validate_patient'),
    url(r'^validate_patient/(?P<appointment_id>[0-9]+)/', views.validate_patient, name='validate_patient'),
    url(r'^login_view/', views.login_view, name='login_view'),
    url(r'^logout_view/', views.logout_view, name='logout_view'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
