from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction as atomic_transaction
from nm.nm_apis import nm_student_progress_update
import uuid
from assessments.models import StudentAssessment

def get_uid():
    uid = str(uuid.uuid4())
    uid = uid[::-1]
    return uid.replace("-", "")[:8]


# Create your models here.


class Course(models.Model):
    course_unique_id = models.CharField(max_length=255, unique=True)
    course_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    status = models.IntegerField(default=1)  # 0 inactive/ 1 - active
    duration = models.IntegerField(default=0)  # in Minute

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.course_unique_id)


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    module_name = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.module_name)


class CourseVideo(models.Model):
    CONTENT_TYPES = (
        (0, 'youtube ID'),
        (1, 'meeting link'),
        (2, 'assessment test'),
        (3, 'project submission'),
        (4, 'hackathon form link'), 
    )
    assessment = models.ForeignKey('assessments.Assessment', on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    course_module = models.ForeignKey(CourseModule, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    y_id = models.CharField(max_length=255, null=True, blank=True)
    # 0 - youtube 
    # 1 - meeting link
    content_type = models.IntegerField(default=0, choices=CONTENT_TYPES)
    link = models.TextField(null=True, blank=True)

    duration = models.IntegerField(default=0)  # in Minute

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    origin = models.IntegerField(null=True, blank=True)  # 0 - NM
    status = models.IntegerField(default=0)
    reference_id = models.CharField(max_length=255, null=True, blank=True, default=get_uid())

    progress_percentage = models.FloatField(default=0)

    online_score = models.FloatField(default=0)
    offline_score = models.FloatField(default=0)
    project_score = models.FloatField(default=0)

    assessment_status = models.BooleanField(default=False)
    course_complete = models.BooleanField(default=False)
    certificate_issued = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.course) + " - " + str(self.user)


@receiver(pre_save, sender=Subscription)
def update_progress_percentage(sender, instance, **kwargs):
    instance.progress_percentage = instance.online_score + instance.offline_score + instance.project_score

#
# @receiver(post_save, sender=Subscription)
# def update_progress_to_nm(sender, instance, **kwargs):
#     """
#     Update NM Portal level with student progress percentage
#     """
#     try:
#         if instance.origin == 0:
#             assessment_list = StudentAssessment.objects.filter(
#                 course_id=instance.course_id,
#                 user_id=instance.user_id
#             ).order_by('-id')
#
#             serial_number = assessment_list.count()
#             last_assessment = assessment_list.first()
#
#             total_questions = last_assessment.total_questions_count if last_assessment else 0
#             correct_answers = last_assessment.correct_answer_count if last_assessment else 0
#             score_percentage = (correct_answers/total_questions) * 100
#             refer_id = last_assessment.id if last_assessment else ''
#             nm_update = nm_student_progress_update(
#                 student_id=instance.user.username,
#                 course_unique_code=instance.course.course_unique_id,
#                 total_score=f"{instance.progress_percentage}",
#                 certificate_issued="true" if instance.certificate_issued else "false",
#                 assessment_status="true" if instance.assessment_status else "false",
#                 course_complete="true" if instance.course_complete else "false",
#                 assessment_data={
#                    "total_questions": total_questions,
#                    "correct_answers": correct_answers,
#                    "score": score_percentage,
#                    "created": last_assessment.created_at.strftime("%Y-%m-%d %H:%M:%S") if last_assessment else None,
#                    "updated": last_assessment.updated_at.strftime("%Y-%m-%d %H:%M:%S") if last_assessment else None,
#                    "reference": "igcdd" + str(refer_id),
#                    "serial": serial_number,
#                    "attempt": 1
#                }
#
#            )
#     except Exception as e:
#         print("NM Progress update issue", str(e))


class UserWatchedVideo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    video = models.ForeignKey(CourseVideo, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.course)
