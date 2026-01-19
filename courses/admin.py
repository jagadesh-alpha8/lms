from django.contrib import admin
from .models import Course, CourseModule, CourseVideo, Subscription, UserWatchedVideo
import requests
from nm.nm_apis import nm_keys
import json


# Register your models here.

def publish_course(modeladmin, request, queryset):
    for course in queryset:
        print(course)
        url = "https://api.naanmudhalvan.tn.gov.in/api/v1/lms/client/course/publish/"
        payload = {
            "course_unique_code": course.course_unique_id,
            "course_name": course.course_name,
            "course_description": course.description,
            "course_image_url": course.image.url,
            "instructor": "Ingage",
            "duration": str(course.duration),
            "number_of_videos": "45",
            "language": "english",
            "main_stream": "engineering",
            "sub_stream": "cse",
            "category": "Python",
            "system_requirements": "Basic understanding of another programming language - Javascript, Ruby, C#, PHP, or similar",
            "has_subtitles": "true",
            "reference_id": "2022/06/23/001",
            "course_type": "ONLINE",
            "location": ""
        }

        access_key, refresh_key = nm_keys()
        if access_key:
            headers = {
                'Authorization': f'Bearer {access_key}',
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, json=payload)

publish_course.short_description = 'Publish Course'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_unique_id', 'course_name', 'status', 'duration', 'created_at', 'updated_at']
    list_filter = ['status']
    search_fields = ['course_unique_id']
    actions = [publish_course]


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'module_name', 'created_at', 'updated_at']
    search_fields = ['module_name', 'course__course_unique_id']


@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'course', 'course_module', 'y_id', 'duration', 'created_at', 'updated_at']
    search_fields = ['title']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    #    list_display = ['id', 'course', 'user', 'origin', 'progress_percentage','online_score', 'offline_score', 'project_score', 'created_at', 'updated_at']
    readonly_fields = ['progress_percentage']
    search_fields = ['user__username']


@admin.register(UserWatchedVideo)
class UserWatchedVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course', 'video', 'created_at', 'updated_at']

# @admin.register()
# class Admin(admin.ModelAdmin):
#     list_display = ['id', 'created_at', 'updated_at']
#     list_filter = []
#     search_fields = []
