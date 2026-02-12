from django.shortcuts import render
import threading
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from .forms import RegistrationForm


FORM_TITLES = {
    "iot_sensor": "IOT and Sensor Integration",
    "info_network_cabling": "Information Network Cabling",
    "it_network_admin": "IT Network System Administrator",
    "cybersec_ibm": "Cyber Security Essentials with IBM Certification",
    "ev_tech": "EV Technology",
    "embedded_c_mc": "Embedded C & Micro Controller Programming",
    "iot_esp32": "IoT Application (ESP32)",
    "network_essentials": "Network Essentials",
}

def async_post_save(instance):
    # any heavy work: mail, logs, analytics, background tasks
    pass

@csrf_exempt
def registration_view(request, form_type=None):

    if form_type not in FORM_TITLES:
        raise Http404("Form not found")

    form_title = FORM_TITLES[form_type]

    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():

            # SAVE FILES SYNCHRONOUSLY (VERY IMPORTANT)
            instance = form.save(commit=False)
            instance.form_title = form_type
            instance.save()

            # ASYNC background jobs (safe)
            threading.Thread(
                target=async_post_save,
                args=(instance,),
                daemon=True
            ).start()

            return render(request, "success.html")

    else:
        form = RegistrationForm()

    return render(request, "form.html", {
        "form": form,
        "form_title": form_title
    })

from django.http import JsonResponse
from .models import District, College

def load_districts(request):
    zone_id = request.GET.get('zone_id')
    districts = District.objects.filter(zone_id=zone_id).order_by('name')
    data = [{"id": d.id, "name": d.name} for d in districts]
    return JsonResponse(data, safe=False)

def load_colleges(request):
    district_id = request.GET.get('district_id')
    colleges = College.objects.filter(district_id=district_id).order_by('name')
    data = [{"id": c.id, "name": c.name} for c in colleges]
    return JsonResponse(data, safe=False)
