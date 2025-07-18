from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import courses
from django.db import transaction as atomic_transaction
from nm.nm_apis import nm_student_progress_update
# Create your models here.


class Assessment(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    serial = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + " - " + str(self.name)


class AssessmentQuestion(models.Model):
    CORRECT_ANSWERS = (
        (1, 'option_1'),
        (2, 'option_2'),
        (3, 'option_3'),
        (4, 'option_4'),
    )
    assessment = models.ForeignKey(Assessment, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.TextField(null=True, blank=True)
    option_1 = models.TextField(null=True, blank=True)
    option_2 = models.TextField(null=True, blank=True)
    option_3 = models.TextField(null=True, blank=True)
    option_4 = models.TextField(null=True, blank=True)
    correct_answer = models.IntegerField(null=True, blank=True, choices=CORRECT_ANSWERS)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + " - " + str(self.question)


class StudentAssessment(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.SET_NULL, null=True, blank=True)
    course_video = models.ForeignKey('courses.CourseVideo', on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    total_questions_count = models.IntegerField(default=0)
    correct_answer_count = models.IntegerField(default=0)
    wrong_answer_count = models.IntegerField(default=0)
    data = models.JSONField(null=True, blank=True)
    attempt = models.IntegerField(default=0)

    api_send = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + " - " + str(self.assessment)


@receiver(post_save, sender=StudentAssessment)
def update_student_progress(sender, instance, **kwargs):

    with atomic_transaction.atomic():
        try:
            try:
                subscription = courses.models.Subscription.objects.select_for_update().get(
                    user_id=instance.user_id,
                    course_id=instance.course_id,
                )
            except courses.models.Subscription.DoesNotExist:
                subscription = courses.models.Subscription.objects.create(
                    user_id=instance.user_id,
                    course_id=instance.course_id,
                    origin=0
                )

            total_online_score = 0
            std_assessments_list = StudentAssessment.objects.filter(course_id=instance.course_id,user_id=instance.user_id,)
            new_total_score = 0
            assessment_ids = std_assessments_list.values_list('assessment_id', flat=True)
            assessment_ids = list(set(assessment_ids)) if assessment_ids else []
            for assessment_id in assessment_ids:
                std_ass = std_assessments_list.filter(assessment_id=assessment_id).order_by('-created_at').first()
                total_online_score += std_ass.correct_answer_count
                new_total_score += (std_ass.correct_answer_count/std_ass.total_questions_count) * 100
            subscription.online_score = total_online_score
            subscription.save()

            if subscription.origin == 0 and assessment_ids:
                serial_number = instance.assessment.serial if instance.assessment_id else ''

                total_questions = instance.total_questions_count
                correct_answers = instance.correct_answer_count
                score_percentage = (correct_answers/total_questions) * 100
                refer_id = instance.id if instance else ''
                total_score = new_total_score/ 4
                nm_update = nm_student_progress_update(
                    student_id=subscription.user.username,
                    course_unique_code=subscription.course.course_unique_id,
                    total_score=f"{total_score}",
                    certificate_issued="true" if subscription.certificate_issued else "false",
                    assessment_status="true" if subscription.assessment_status else "false",
                    course_complete="true" if subscription.course_complete else "false",
                    assessment_data={
                        "total_questions": total_questions,
                        "correct_answers": correct_answers,
                        "score": score_percentage,
                        "created": instance.created_at.strftime("%Y-%m-%d %H:%M:%S") if instance else None,
                        "updated": instance.updated_at.strftime("%Y-%m-%d %H:%M:%S") if instance else None,
                        "reference": "igcdd" + str(refer_id),
                        "serial": serial_number,
                        "attempt": instance.attempt
                    }

                )
        except Exception as e:
            print("Signal Error", e)



