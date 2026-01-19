import json
from django.db.models import F, Sum, IntegerField
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from courses.models import Course, CourseModule, CourseVideo, UserWatchedVideo, Subscription
from rest_framework import status
from rest_framework.response import Response
import uuid

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from users.decorators import user_access_check
from users.models import UserRoles
from .models import Assessment, AssessmentQuestion, StudentAssessment
import random


@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.STUDENT])
def assessment_info(request):
    """
    :param request:
    :param assessment_id:
    :param course_id:
    :return:
    """
    course_id = request.POST.get('course_id', None)
    assessment_id = request.POST.get('assessment_id', None)
    if course_id is None or assessment_id is None:
        return Response({"message": "Please provide course_id/ assessment_id"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        subscription = Subscription.objects.get(user_id=request.user.id, course_id=course_id)
        course_video = CourseVideo.objects.get(course_id=subscription.course_id, assessment_id=assessment_id)
        assessment = course_video.assessment
        try:
            student_assessment = StudentAssessment.objects.get(
                user_id=request.user.id,
                assessment_id=assessment_id, course_id=course_id)
            context = {
                "is_done": True,
                "assessment_id": assessment.id,
                "assessment_name": assessment.name,
                "total_questions_count": student_assessment.total_questions_count,
                "correct_answer_count": student_assessment.correct_answer_count,
                "wrong_answer_count": student_assessment.wrong_answer_count,
                "questions": student_assessment.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        except StudentAssessment.DoesNotExist:
            final_question_list = []
            assessment_questions = AssessmentQuestion.objects.filter(assessment_id=assessment.id)
            for question in assessment_questions:
                options_list = [
                    {"option": 1, "value": question.option_1},
                    {"option": 2, "value": question.option_2},
                    {"option": 3, "value": question.option_3},
                    {"option": 4, "value": question.option_4},
                ]
                random.shuffle(options_list)
                temp = {
                    "question_id": question.id,
                    "question": question.question,
                    'correct_answer': question.correct_answer,
                    "options": options_list
                }
                final_question_list.append(temp)
            random.shuffle(final_question_list)
            context = {
                "is_done": False,
                "assessment_id": assessment.id,
                "assessment_name": assessment.name,
                "questions": final_question_list,
                'total_marks': assessment_questions.count()
            }
            return Response(context, status=status.HTTP_200_OK)
    except Course.DoesNotExist:
        return Response({"message": "Please provide valid course id"}, status=status.HTTP_400_BAD_REQUEST)

    except Subscription.DoesNotExist:
        return Response({"message": "Please subscribe to the course"}, status=status.HTTP_400_BAD_REQUEST)

    except CourseVideo.DoesNotExist:
        return Response({"message": "Please provide valid assessment_id"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.STUDENT])
def assessment_submission(request):
    """
    :param request:
    :param assessment_id:
    :param data:
    :return:
    """
    course_id = request.POST.get('course_id', None)
    assessment_id = request.POST.get('assessment_id', None)
    data = request.POST.get('data', None)
    if data:
        try:
            data = json.loads(data)
        except:
            data = None
    if course_id is None or assessment_id is None or data is None:
        return Response({"message": "Please provide course_id/ assessment_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        subscription = Subscription.objects.get(user_id=request.user.id, course_id=course_id)
        course_video = CourseVideo.objects.get(course_id=subscription.course_id, assessment_id=assessment_id)
        assessment = course_video.assessment
        total_questions_count = 0
        correct_answer_count = 0
        wrong_answer_count = 0
        for index, record in enumerate(data):
            try:
                question = AssessmentQuestion.objects.get(id=record['question_id'], assessment_id=assessment_id)
                if question.correct_answer == int(record['selected_option']):
                    correct_answer_count += 1
                else:
                    wrong_answer_count += 1
                total_questions_count += 1
                data[index]['correct_answer'] = question.correct_answer
            except AssessmentQuestion.DoesNotExist:
                return Response({"message": "Please provide valid data"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"message": "Please provide valid data", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            get_student_assessment = StudentAssessment.objects.get(
                user_id=request.user.id, course_id=course_id, assessment_id=assessment_id)
            get_student_assessment.data = data
            get_student_assessment.attempt += 1
            get_student_assessment.save()

            context = {
                "message": "submitted successfully",
                'total_questions_count': total_questions_count,
                'correct_answer_count': correct_answer_count,
                'wrong_answer_count': wrong_answer_count,
                "assessment_id": assessment.id,
                "assessment_name": assessment.name,
            }
            return Response(context, status=status.HTTP_200_OK)

        except StudentAssessment.DoesNotExist:
            new_student_assessment = StudentAssessment.objects.create(
                assessment_id=assessment_id,
                course_video_id=course_video.id,
                course_id=course_id,
                user_id=request.user.id,
                total_questions_count=total_questions_count,
                correct_answer_count=correct_answer_count,
                wrong_answer_count=wrong_answer_count,
                data=data,
                attempt=1
            )
            context = {
                "message": "submitted successfully",
                'total_questions_count': total_questions_count,
                'correct_answer_count': correct_answer_count,
                'wrong_answer_count': wrong_answer_count,
                "assessment_id": assessment.id,
                "assessment_name": assessment.name,
            }
            return Response(context, status=status.HTTP_200_OK)

    except Course.DoesNotExist:
        return Response({"message": "Please provide valid course id"}, status=status.HTTP_400_BAD_REQUEST)

    except Subscription.DoesNotExist:
        return Response({"message": "Please subscribe to the course"}, status=status.HTTP_400_BAD_REQUEST)

    except CourseVideo.DoesNotExist:
        return Response({"message": "Please provide valid assessment_id"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.ADMIN])
def assessments_report(request):
    """
    :param request:
    :param course_id:
    :return assessments list report of total_students_count & attempts details:
    """
    course_id = request.GET.get('course_id', None)
    if course_id is None:
        return Response({"message": "Please provide course_id"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        course = Course.objects.get(id=course_id)
        assessment_ids = CourseVideo.objects.values_list('assessment_id', flat=True).filter(course_id=course_id).order_by('id')

        assessments_list = Assessment.objects.filter(id__in=assessment_ids)
        subscribed_students_count = Subscription.objects.filter(course_id=course_id).count()
        final_assessment_records = []
        for assessment in assessments_list:

            student_assessments = StudentAssessment.objects.filter(
                assessment_id=assessment.id,
                course_id=course_id
            )
            min_40_percentage_scored_count = 0
            for std in student_assessments:
                total_questions_count = std.total_questions_count
                correct_answer_count = std.correct_answer_count
                score_percentage = (correct_answer_count/ total_questions_count) * 100
                if score_percentage >= 40:
                    min_40_percentage_scored_count += 1
            student_assessments_count = student_assessments.count()
            attempt_percentage = (student_assessments_count / subscribed_students_count) * 100
            temp = {
                "assessment_id": assessment.id,
                "assessment": assessment.name,
                "total_students_count": subscribed_students_count,
                "attempt_students_count": student_assessments_count,
                "attempt_percentage": round(attempt_percentage, 2),
                "min_40_percentage_scored_count": min_40_percentage_scored_count,
            }
            final_assessment_records.append(temp)
        context = {
            "assessments_list": final_assessment_records,
            "total_assessment_count": assessments_list.count(),
            "course": {
                "id": course.id,
                "course_unique_id": course.course_unique_id,
                "course_name": course.course_name,
                "description": course.description,
                "image": course.image.url if course.image else None,
                "duration": course.duration,
                "status": course.status,
                "created_at": course.created_at,
                "updated_at": course.updated_at,
            }
        }
        return Response(context, status=status.HTTP_200_OK)

    except Course.DoesNotExist:
        return Response({"message": "Please provide valid course_id"}, status=status.HTTP_400_BAD_REQUEST)

