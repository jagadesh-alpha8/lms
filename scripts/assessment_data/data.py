from django.conf import settings
import os
import csv
from users.models import User
from assessments.models import Assessment, StudentAssessment
final_data = []
total = 4005

assessment_file = open(os.path.join(settings.BASE_DIR, 'scripts/assessment_data_2023_01_12.csv'), 'w')
writer = csv.writer(assessment_file)
#with open(os.path.join(settings.BASE_DIR, 'scripts/assessment_data/new_latest.csv')) as file:

with open(os.path.join(settings.BASE_DIR, 'scripts/assessment_data/9_students.csv')) as file:
    csv_data = csv.reader(file)
    index = 0
    writer.writerow(next(csv_data) + ['Assessment 1', 'Assessment 2', 'Assessment 3', 'Assessment 4'])
    for record in csv_data:
        index += 1
        as_1 = 0
        as_2 = 0
        as_3 = 0
        as_4 = 0

        student_id = record[1]
        try:
            user = User.objects.get(username=student_id)
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
            as_1 = as_2 = as_3 = error
        except User.MultipleObjectsReturned:
            error = "More students found"
            as_1 = as_2 = as_3 = as_4 = error

        record += [as_1, as_2, as_3, as_4]
        writer.writerow(record)
        print("Pending - ", total - index)




