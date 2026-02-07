import json

import requests
import os
from django.conf import settings


NM_BASE_URL = "https://api.naanmudhalvan.tn.gov.in/api/v1/lms/client"


def nm_keys():
    url = f"{NM_BASE_URL}/token/"

    payload = {
        'client_key': settings.NM_CLIENT_KEY,
        'client_secret': settings.NM_CLIENT_SECRET
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    (payload)
    print(response.text)
    print(response.status_code)
    data = response.json()
    access_key = data['token'] if "token" in data else None
    refresh_key = data['refresh'] if "refresh" in data else None
    return access_key, refresh_key


def nm_student_progress_update(
        student_id: str,
        course_unique_code: str,
        total_score: str,
        certificate_issued: str,
        assessment_status: str,
        course_complete: str,
        assessment_data: dict = None,
):
    url = f"{NM_BASE_URL}/course/xf/"

    payload = {
        "user_unique_id": student_id,
        "course_unique_code": course_unique_code,
        "total_score": total_score,
        "certificate_issued": certificate_issued,
        "assessment_status": assessment_status,
        "course_complete": course_complete,
        "assessment_data": assessment_data,
    }
    access_key, refresh_key = nm_keys()
    print('access_key', access_key)
    print('refresh_key', refresh_key)
    print(payload)
    if access_key:
        headers = {
            'Authorization': f'Bearer {access_key}'
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        print(response.text)
        print(response.status_code)
