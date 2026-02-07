from django.urls import path
from .courses.views import course,course_list, course_details
from .course_modules.views import course_module, course_module_list
from .course_videos.views import course_video, course_video_list
from .watched_videos.views import update_course_watched_video

urlpatterns = [
    path('list/', course_list),
    path('course/', course),
    path('course/details/', course_details),
    path('course/module/', course_module),
    path('course/module/list/', course_module_list),
    path('course/video/', course_video),
    path('course/video/list/', course_video_list),
    path('course/video/watched/update/', update_course_watched_video),
]
