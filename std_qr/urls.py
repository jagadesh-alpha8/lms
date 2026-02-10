from django.urls import path
from .views import registration_view

urlpatterns = [

    path('iot-sensor/', registration_view, {'form_type': 'iot_sensor'}, name='iot-sensor-form'),
    path('info-network-cabling/', registration_view, {'form_type': 'info_network_cabling'}, name='info-network-cabling-form'),
    path('it-network-admin/', registration_view, {'form_type': 'it_network_admin'}, name='it-network-admin-form'),
    path('cybersec-ibm/', registration_view, {'form_type': 'cybersec_ibm'}, name='cybersec-ibm-form'),
    path('ev-technology/', registration_view, {'form_type': 'ev_tech'}, name='ev-technology-form'),
    path('embedded-c-mc/', registration_view, {'form_type': 'embedded_c_mc'}, name='embedded-c-mc-form'),
    path('iot-esp32/', registration_view, {'form_type': 'iot_esp32'}, name='iot-esp32-form'),
    path('network-essentials/', registration_view, {'form_type': 'network_essentials'}, name='network-essentials-form'),
]
