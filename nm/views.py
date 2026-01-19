from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from courses.models import Course, Subscription
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from users.models import User, UserRoles
from .models import TempToken
from django.conf import settings
from datetime import datetime, timedelta
import jwt


@api_view(['POST'])
def token(request):
    client_key = request.data.get('client_key', None)
    client_secret = request.data.get('client_secret', None)
    if client_key is None or client_secret is None:
        return Response({"message": "Please provide client_key/ client_secret"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    user = authenticate(username=client_key, password=client_secret)
    if user:
        if user.account_role == UserRoles.NM_USER:
            refresh_token = TokenObtainPairSerializer.get_token(user)
            context = {
                'access_key': str(refresh_token.access_token),
                'refresh_key': str(refresh_token),
            }
            return Response(context, status=status.HTTP_200_OK, content_type='application/json')
    return Response({"message": "Please provide valid client_key/ client_secret"}, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['POST'])
def token_refresh(request):
    refresh = request.data.get('refresh', None)
    if refresh is None:
        return Response({"message": "Please provide refresh"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    new_refresh = RefreshToken(refresh)
    context = {
        "refresh_key": str(new_refresh),
        "access_key": str(new_refresh.access_token),
    }
    return Response(context, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def course_subscribe(request):
    student_id = request.data.get('user_id', None)
    course_id = request.data.get('course_id', None)

    print(student_id, course_id)
    if course_id is None or student_id is None:
        return Response({

            "subscription_registration_status": False,
            "error": "Please provide student_id/ course_id"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    try:
        get_course = Course.objects.get(course_unique_id=course_id)
        try:
            student_user = User.objects.get(username__iexact=student_id, account_role=UserRoles.STUDENT)
        except User.DoesNotExist:
            student_user = User.objects.create(
                username=student_id,
                email=str(student_id) + "@nm.tn.gov.in",
                account_role=UserRoles.STUDENT,
                origin=0
            )

        try:
            subscription = Subscription.objects.get(user_id=student_user.id, course_id=get_course.id)
            context = {
                "subscription_registration_status": False,
                "error": "Already subscribed"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        except Subscription.DoesNotExist:
            subscription = Subscription.objects.create(
                user_id=student_user.id,
                course_id=get_course.id,
                origin=0
            )

            context = {
                "subscription_registration_status": True,
                "subscription_reference_id": subscription.reference_id
            }
            return Response(context, status=status.HTTP_200_OK, content_type='application/json')

    except Course.DoesNotExist:
        context = {
            "subscription_registration_status": False,
            "error": "Please provide valid course_id"
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def course_access_url(request):
    student_id = request.data.get('user_id', None)
    course_id = request.data.get('course_id', None)

    print(student_id, course_id)
    if course_id is None or student_id is None:
        return Response({
            "access_status": True,
            "error": "Please provide student_id/ course_id"}, status=status.HTTP_200_OK, content_type='application/json')

    try:
        get_course = Course.objects.get(course_unique_id=course_id)
        try:
            student_user = User.objects.get(username__iexact=student_id, account_role=UserRoles.STUDENT)
        except User.DoesNotExist:
            student_user = User.objects.create(
                username=student_id,
                email=str(student_id) + "nm.tn.gov.in",
                account_role=UserRoles.STUDENT,
                origin=0
            )

        try:
            subscription = Subscription.objects.get(user_id=student_user.id, course_id=get_course.id)
            old_temp_token_update = TempToken.objects.filter(
                user_id=student_user.id,
                course_id=get_course.id,
                status=0
            ).update(status=2)
            new_token = TempToken.objects.create(
                user_id=student_user.id,
                course_id=get_course.id,
                status=0
            )

            dt = datetime.now() + timedelta(days=1)

            encoded_jwt = jwt.encode({
                "student_id": student_id,
                "course_id": course_id,
                "key": new_token.token,
                "exp": dt
                  }, str(settings.NM_JWT_SECRET), algorithm="HS256")

            frontend_url = "http://app.ingagemetaverse.com/nm/redirect/?token=" + str(encoded_jwt)
            context = {
                "access_status": True,
                "access_url": frontend_url
            }
            return Response(context, status=status.HTTP_200_OK, content_type='application/json')

        except Subscription.DoesNotExist:
            context = {
                "access_status": False,
                "error": "Please subscribe the course"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    except Course.DoesNotExist:
        context = {
            "access_status": False,
            "error": "Please provide valid course_id"
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

