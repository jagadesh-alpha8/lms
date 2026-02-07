from users.models import User
import csv
import os
from django.conf import settings
from assessments.models import StudentAssessment
from courses.models import Subscription

filename = "scripts/assessment_data/2023_01_13.csv"
assessment_file = open(os.path.join(settings.BASE_DIR, 'scripts/assessment_data_update_13_01_23.csv'), 'w')
writer = csv.writer(assessment_file)
total_counter = 32
with open(os.path.join(settings.BASE_DIR, filename), 'r') as file:
    csv_data = csv.reader(file)
    writer.writerow(next(csv_data))
    index = 0

    for row in csv_data:
        """
        0 S.NO,
        1 roll_no,
        2 nm_id,
        3 student_name,
        4 college_code,
        5 college_name,
        6 Assessment 1,Assessment 2,Assessment 3, Assessment 4

        """
        index += 1
        student_id = row[2]
        score_1 = row[6]
        score_2 = row[7]
        score_3 = row[8]
        score_4 = row[9]
        course_complete = False

        print("Pending -- ", total_counter - index, student_id)
        try:
            try:
                user = User.objects.get(username=student_id)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=student_id,
                       email=str(student_id) + "@nm.tn.gov.in",
                       account_role=1,
                       origin=0
                   )

            try:
                subscription = Subscription.objects.get(
                    user_id=user.id,
                    course_id=1,
                )
            except Subscription.DoesNotExist:
                subscription = Subscription.objects.create(
                    user_id=user.id,
                    course_id=1,
                    origin=0
                )

            subscription.course_complete = True if str(course_complete).lower() == 'true' else subscription.course_complete
            subscription.save()
            if score_1:
                total_questions = 5
                correct_answer_count = int((float(score_1)/100) * total_questions)
                try:
                    assessment_1 = StudentAssessment.objects.get(
                        assessment_id=3,
                        user_id=user.id,
                        course_id=1
                    )

                    if assessment_1.correct_answer_count != correct_answer_count:
                        assessment_1.correct_answer_count = correct_answer_count
                        assessment_1.wrong_answer_count = total_questions - correct_answer_count
                        assessment_1.attempt += 1
                        assessment_1.save()
                except StudentAssessment.MultipleObjectsReturned:

                    assessment_1s = StudentAssessment.objects.filter(
                        assessment_id=3,
                        user_id=user.id,
                        course_id=1
                    )
                    for assessment_1 in assessment_1s:

                        if assessment_1.correct_answer_count != correct_answer_count:
                            assessment_1.correct_answer_count = correct_answer_count
                            assessment_1.wrong_answer_count = total_questions - correct_answer_count
                            assessment_1.attempt += 1
                            assessment_1.save()

                except StudentAssessment.DoesNotExist:
                    assessment_1 = StudentAssessment.objects.create(
                        assessment_id=3,
                        user_id=user.id,
                        course_id=1,
                        total_questions_count=total_questions,
                        correct_answer_count=correct_answer_count,
                        wrong_answer_count=total_questions - correct_answer_count,
                        attempt=1
                    )

            if score_2:
                total_questions = 10
                correct_answer_count = int((float(score_2)/100) * total_questions)
                try:
                    assessment = StudentAssessment.objects.get(
                        assessment_id=4,
                        user_id=user.id,
                        course_id=1
                    )

                    if assessment.correct_answer_count != correct_answer_count:
                        assessment.correct_answer_count = correct_answer_count
                        assessment.wrong_answer_count = total_questions - correct_answer_count
                        assessment.attempt += 1
                        assessment.save()

                except StudentAssessment.MultipleObjectsReturned:

                    assessments = StudentAssessment.objects.filter(
                        assessment_id=4,
                        user_id=user.id,
                        course_id=1
                    )

                    for assessment in assessments:

                        if assessment.correct_answer_count != correct_answer_count:
                            assessment.correct_answer_count = correct_answer_count
                            assessment.wrong_answer_count = total_questions - correct_answer_count
                            assessment.attempt += 1
                            assessment.save()

                except StudentAssessment.DoesNotExist:
                    assessment = StudentAssessment.objects.create(
                        assessment_id=4,
                        user_id=user.id,
                        course_id=1,
                        total_questions_count=total_questions,
                        correct_answer_count=correct_answer_count,
                        wrong_answer_count=total_questions - correct_answer_count,
                        attempt=1
                    )

            if score_3:
                total_questions = 10
                correct_answer_count = int((float(score_3)/100) * total_questions)
                try:
                    assessment = StudentAssessment.objects.get(
                        assessment_id=6,
                        user_id=user.id,
                        course_id=1
                    )

                    if assessment.correct_answer_count != correct_answer_count:
                        assessment.correct_answer_count = correct_answer_count
                        assessment.wrong_answer_count = total_questions - correct_answer_count
                        assessment.attempt += 1
                        assessment.save()
                except StudentAssessment.MultipleObjectsReturned:

                    assessments = StudentAssessment.objects.filter(
                        assessment_id=6,
                        user_id=user.id,
                        course_id=1
                    )
                    for assessment in assessments:

                        if assessment.correct_answer_count != correct_answer_count:
                            assessment.correct_answer_count = correct_answer_count
                            assessment.wrong_answer_count = total_questions - correct_answer_count
                            assessment.attempt += 1
                            assessment.save()

                except StudentAssessment.DoesNotExist:
                    assessment = StudentAssessment.objects.create(
                        assessment_id=6,
                        user_id=user.id,
                        course_id=1,
                        total_questions_count=total_questions,
                        correct_answer_count=correct_answer_count,
                        wrong_answer_count=total_questions - correct_answer_count,
                        attempt=1
                    )

            if score_4:
                total_questions = 25
                correct_answer_count = int((float(score_4)/100) * total_questions)
                try:
                    assessment = StudentAssessment.objects.get(
                        assessment_id=7,
                        user_id=user.id,
                        course_id=1
                    )

                    if assessment.correct_answer_count != correct_answer_count:
                        assessment.total_questions = total_questions
                        assessment.correct_answer_count = correct_answer_count
                        assessment.wrong_answer_count = total_questions - correct_answer_count
                        assessment.attempt += 1
                        assessment.save()

                except StudentAssessment.MultipleObjectsReturned:

                    assessments = StudentAssessment.objects.filter(
                        assessment_id=7,
                        user_id=user.id,
                        course_id=1
                    )
                    for assessment in assessments:
                        if assessment.correct_answer_count != correct_answer_count:

                            assessment.total_questions = total_questions
                            assessment.correct_answer_count = correct_answer_count
                            assessment.wrong_answer_count = total_questions - correct_answer_count
                            assessment.attempt += 1
                            assessment.save()

                except StudentAssessment.DoesNotExist:
                    assessment = StudentAssessment.objects.create(
                        assessment_id=7,
                        user_id=user.id,
                        course_id=1,
                        total_questions_count=total_questions,
                        correct_answer_count=correct_answer_count,
                        wrong_answer_count=total_questions - correct_answer_count,
                        attempt=1
                    )

            writer.writerow(row)

            print("Pending -- ", total_counter - index, student_id)
        except User.DoesNotExist:
            writer.writerow(row + ['User not found'])
        except Exception as e:
            writer.writerow(row + ['Error - ' + str(e)])

            print("Pending -- Error ----<> ", str(e))
