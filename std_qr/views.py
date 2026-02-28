from django.views.decorators.cache import never_cache
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

@never_cache
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

import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Registration
from .filters import RegistrationFilter


def registration_list(request):
    queryset = Registration.objects.select_related(
        'zone', 'district', 'college'
    ).all().order_by('-created_at')

    filterset = RegistrationFilter(request.GET, queryset=queryset)
    filtered_qs = filterset.qs

    # Export CSV (ALL filtered data, no pagination)
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="registrations.csv"'

        writer = csv.writer(response)

        field_names = [field.name for field in Registration._meta.fields]
        writer.writerow(field_names)

        for obj in filtered_qs:
            row = []
            for field in field_names:
                value = getattr(obj, field)

                # Show readable names for foreign keys
                if field in ['zone', 'district', 'college']:
                    value = str(value) if value else ''

                row.append(value)

            writer.writerow(row)

        return response

    # Django Pagination (20 per page)
    paginator = Paginator(filtered_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'registration_list.html', {
        'filter': filterset,
        'registrations': page_obj,
        'page_obj': page_obj,
        'request': request
    })
