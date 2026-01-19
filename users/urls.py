from django.urls import path
from .views import student_token, login, profile, token_refresh

urlpatterns = [
    path('token/validation/nm/', student_token),
    path('login/', login),
    path('token/refresh/', token_refresh),
    path('profile/', profile),
]
