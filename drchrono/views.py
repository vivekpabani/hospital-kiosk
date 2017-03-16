from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Doctor

@login_required
def home(request):
    """
    home view where user-doctor lands after authorizing with drchrono.
    if it is first visit of doctor, then redirect to kiosk pin set up,
    otherwise redirect to kiosk.
    """

    access_token = request.user.social_auth.get(provider='drchrono').extra_data['access_token']

    # if doctor's first time on kiosk, ask to set up pin. 
    if not Doctor.objects.filter(user=request.user):
        return redirect('/set_kiosk_pin')

    request.session['kiosk_pin_set'] = True
    return redirect('/kiosk')

def set_kiosk_pin(request):
    """
    process kiosk pin form, and set up if valid pin.
    redirect to home if setup successfully.
    """    

    return HttpResponse('Pin Setup')

def kiosk(request):
    """
    Display today's appointments with option to check in.
    Also provide option to toggle between doctor's kiosk.
    """

    return HttpResponse('Kiosk')


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
