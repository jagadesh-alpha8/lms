from django.conf import settings
import os
import csv
from users.models import User
from assessments.models import Assessment, StudentAssessment
final_data = []
total = 4005

assessment_file = open(os.path.join(settings.BASE_DIR, 'scripts/student_data_030123.csv'), 'w')
writer = csv.writer(assessment_file)
#with open(os.path.join(settings.BASE_DIR, 'scripts/assessment_data/new_latest.csv')) as file:

users = User.objects.filter(account_role=1, origin=0)
total = users.count()

index = 0
writer.writerow(['Student_id', 'Assessment 1', 'Assessment 2', 'Assessment 3', 'Assessment 4'])
for index, user in enumerate(users):

    try:
        user = user
        try:
            assessment = StudentAssessment.objects.filter(
                assessment_id=3, user_id=user.id
            ).order_by('-created_at').first()
            if assessment:
                as_1 = (assessment.correct_answer_count/ assessment.total_questions_count) * 100
            else:
                as_1 = 'No Assessment'
        except StudentAssessment.DoesNotExist:
            as_1 = 'No Assessment'

        try:
            assessment = StudentAssessment.objects.filter(
                assessment_id=4, user_id=user.id
            ).order_by('-created_at').first()
            if assessment:
                as_2 = (assessment.correct_answer_count/ assessment.total_questions_count) * 100
            else:
                as_2 = 'No Assessment'
        except StudentAssessment.DoesNotExist:
            as_2 = 'No Assessment'

        try:
            assessment = StudentAssessment.objects.filter(
                assessment_id=6, user_id=user.id
            ).order_by('-created_at').first()
            if assessment:
                as_3 = (assessment.correct_answer_count/ assessment.total_questions_count) * 100
            else:
                as_3 = 'No Assessment'

        except StudentAssessment.DoesNotExist:
            as_3 = 'No Assessment'
        try:
            assessment = StudentAssessment.objects.filter(
                assessment_id=7, user_id=user.id
            ).order_by('-created_at').first()
            if assessment:
                as_4 = (assessment.correct_answer_count/ assessment.total_questions_count) * 100
            else:
                as_4 = 'No Assessment'

        except StudentAssessment.DoesNotExist:
            as_4 = 'No Assessment'

    except User.DoesNotExist:
        error = "No student"
        as_1 = as_2 = as_3 = as_4 = error
    except User.MultipleObjectsReturned:
        error = "More students found"
        as_1 = as_2 = as_3 = as_4 = error

    record = [user.username, as_1, as_2, as_3, as_4]
    writer.writerow(record)
    print("Pending - ", total - index)




