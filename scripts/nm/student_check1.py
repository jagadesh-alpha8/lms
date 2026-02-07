from assessments.models import Assessment, StudentAssessment
from courses.models import Subscription
import json
from users.models import User
import requests
import os
from django.conf import settings

with open(os.path.join(settings.BASE_DIR, "scripts/nm/student_ids.csv"), 'r') as file:
    data = file.read()
    student_ids = str(data).split(',')
    print("Students Count:", len(student_ids))

    users_list = User.objects.filter(username__in=student_ids)
    print("Users Mapped:", users_list.count())
    user_ids = users_list.values_list('id', flat=True)
    assessments = Assessment.objects.all()
    for assessment in assessments:
        print("------------")
        std_assessment_list = StudentAssessment.objects.filter(
            assessment_id=assessment.id,
            user_id__in=user_ids,
        ).distinct('assessment_id', 'user_id')
        print(assessment.name, std_assessment_list.distinct('user_id', 'assessment_id').count(), sep=" : ")


