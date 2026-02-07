from django.urls import path
from .views import assessment_info, assessment_submission, assessments_report
urlpatterns = [
    path('info/', assessment_info),
    path('submission/', assessment_submission),
    path('course/report/', assessments_report),
    # path('token/', token),
    # path('token/', token),
]
