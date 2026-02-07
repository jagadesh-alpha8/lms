from django.urls import path
from .views import token, token_refresh, course_subscribe, course_access_url

urlpatterns = [
    path('token/', token),
    path('token/refresh/', token_refresh),
    path('course/subscribe/', course_subscribe),
    path('course/access/', course_access_url),
    # path('course/access/'), 
]
