import threading
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegistrationForm
from .models import District, College


FORM_TITLES = {
    "iot_sensor":           "IOT and Sensor Integration - Polytechnic",
    "info_network_cabling": "Information Network Cabling - Polytechnic",
    "it_network_admin":     "IT Network System Administrator - Polytechnic",
    "cybersec_ibm":         "Cyber Security Essentials - Polytechnic",
    "ev_tech":              "EV Technology - Polytechnic",
    "embedded_c_mc":        "Embedded C & Micro Controller Programming - Engineering",
    "iot_esp32":            "IoT Application (ESP32) - Engineering",
    "network_essentials":   "Network Essentials - Engineering",
}


def async_post_save(instance):
    # heavy background work: email, analytics, logs, etc.
    pass


@csrf_exempt
def registration_view(request, form_type=None):

    if form_type not in FORM_TITLES:
        raise Http404("Form not found")

    form_title = FORM_TITLES[form_type]

    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.form_title = form_title   # human-readable title, not the key
            instance.save()

            threading.Thread(
                target=async_post_save,
                args=(instance,),
                daemon=True
            ).start()

            # Redirect after successful save — POST/Redirect/GET pattern.
            # Prevents duplicate submission if the user refreshes the page.
            return redirect('registration_success')

        # form.is_valid() returned False — fall through and re-render with errors

    else:
        form = RegistrationForm()

    return render(request, "form.html", {
        "form": form,
        "form_title": form_title,
    })


def registration_success(request):
    return render(request, "success.html")


def load_districts(request):
    zone_id = request.GET.get('zone_id')
    districts = District.objects.filter(zone_id=zone_id).order_by('name')
    return JsonResponse([{"id": d.id, "name": d.name} for d in districts], safe=False)


def load_colleges(request):
    district_id = request.GET.get('district_id')
    colleges = College.objects.filter(district_id=district_id).order_by('name')
    return JsonResponse([{"id": c.id, "name": c.name} for c in colleges], safe=False)



from rest_framework.decorators import api_view
from .models import Registration
from .serializers import RegistrationFullSerializer
from rest_framework.response import Response

@api_view(['GET'])
def registration_full_api(request):
    registrations = Registration.objects.select_related(
        "zone", "district", "college"
    ).order_by("-created_at")

    serializer = RegistrationFullSerializer(
        registrations,
        many=True,
        context={"request": request}
    )
    return Response(serializer.data)