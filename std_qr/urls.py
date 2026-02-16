from django.urls import path
from .views import *

urlpatterns = [

    path('iot-sensor/', registration_view, {'form_type': 'iot_sensor'}, name='iot-sensor-form'),
    path('info-network-cabling/', registration_view, {'form_type': 'info_network_cabling'}, name='info-network-cabling-form'),
    path('it-network-admin/', registration_view, {'form_type': 'it_network_admin'}, name='it-network-admin-form'),
    path('cybersec-ibm/', registration_view, {'form_type': 'cybersec_ibm'}, name='cybersec-ibm-form'),
    path('ev-technology/', registration_view, {'form_type': 'ev_tech'}, name='ev-technology-form'),
    path('embedded-c-mc/', registration_view, {'form_type': 'embedded_c_mc'}, name='embedded-c-mc-form'),
    path('iot-esp32/', registration_view, {'form_type': 'iot_esp32'}, name='iot-esp32-form'),
    path('network-essentials/', registration_view, {'form_type': 'network_essentials'}, name='network-essentials-form'),
    path('ajax/load-districts/', load_districts, name='ajax_load_districts'),
    path('ajax/load-colleges/', load_colleges, name='ajax_load_colleges'),
    path('success/', registration_success, name='registration_success'),
    path('registration_full/', registration_full_api, name='registration_all'),
    

]
