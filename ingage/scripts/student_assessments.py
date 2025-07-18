from assessments.models import Assessment, StudentAssessment
from courses.models import Subscription
import json

import requests
import os
from django.conf import settings

url = "https://api.naanmudhalvan.tn.gov.in/api/v1/lms/client/course/xf/"
access_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnQiOiJ0bnNkYyIsImNsaWVudF9rZXkiOiJZMlpsTVdJek1tTTNOakUyTldFMk5UQTJaRGd3TnpSaU16TmpNREl6WXpBMVpXUm1aV0UyTkNBZ0xRbyIsImV4cGlyeSI6MTY2NzU2ODY5MH0.udnUDuaZZSHOVBgUS3swHj9jsZPvHimKR43oJHLr4pk"

headers = {
    "Content-Type": "application/json",
    'Authorization': f'Bearer {access_key}'
}

subscriptions_list = Subscription.objects.filter(origin=0)
print(subscriptions_list.count())

assessments_list = Assessment.objects.all().order_by('serial')

for assessment in assessments_list:
    std_assessments = StudentAssessment.objects.filter(assessment_id=assessment.id).order_by(
    ).exclude(data=None, api_send=True)
    print(assessment.id, assessment.name, std_assessments.count(), sep="  |  ")
    for std in std_assessments:
        try:
            subscription = Subscription.objects.get(
                user_id=std.user_id,
                course_id=std.course_id,
            )
            if subscription.origin == 0:
                _serial_number = assessment.serial

                # _serial_number = 1
                # serial_number = StudentAssessment.objects.values_list('id', flat=True).filter(
                #     course_id=std.course_id,
                #     user_id=std.user_id
                # ).order_by('id')
                # if serial_number.count() > 1:
                #     _index = list(serial_number).index(std.id)
                #     if _index or _index == 0:
                #         _serial_number = _index + 1
                #     else:
                #         _serial_number = 1
                # else:
                #     _serial_number = 1

                total_questions = std.total_questions_count
                correct_answers = std.correct_answer_count
                score_percentage = (correct_answers/total_questions) * 100
                refer_id = std.id if std else ''

                payload = {
                    "user_unique_id": subscription.user.username,
                    "course_unique_code":subscription.course.course_unique_id,
                    "total_score":f"{subscription.progress_percentage}",
                    "certificate_issued":"true" if subscription.certificate_issued else "false",
                    "assessment_status":"true" if subscription.assessment_status else "false",
                    "course_complete":"true" if subscription.course_complete else "false",
                    "assessment_data":{
                        "total_questions": total_questions,
                        "correct_answers": correct_answers,
                        "score": score_percentage,
                        "created": std.created_at.strftime("%Y-%m-%d %H:%M:%S") if std else None,
                        "updated": std.updated_at.strftime("%Y-%m-%d %H:%M:%S") if std else None,
                        "reference": "igcdd" + str(refer_id),
                        "serial": _serial_number,
                        "attempt": std.attempt
                    }
                }

                response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
                if not response.status_code == 200:
                    print(response.text)
                    print(response.status_code)
                    StudentAssessment.objects.filter(id=std).update(api_send=True)

        except Exception as e:
            print("Exception - as ", e)


