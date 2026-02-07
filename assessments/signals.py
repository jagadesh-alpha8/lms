from courses.models import Subscription
from django.db import transaction as atomic_transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentAssessment

#
# @receiver(post_save, sender=StudentAssessment)
# def update_student_progress(sender, instance, created, **kwargs):
#
#     with atomic_transaction.atomic():
#         try:
#             subscription = Subscription.objects.select_for_update().get(
#                 user_id=instance.user_id,
#                 course_id=instance.course_id,
#             )
#             total_online_score = 0
#             std_assessments_list = StudentAssessment.objects.filter(course_id=instance.course_id,user_id=instance.user_id,)
#             for std_ass in std_assessments_list:
#                 total_online_score += std_ass.correct_answer_count
#             subscription.online_score = total_online_score
#             subscription.save()
#         except:
#             pass

