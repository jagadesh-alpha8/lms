from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from courses.models import Course, Subscription
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User, UserRoles
from nm.models import TempToken
import jwt
from django.conf import settings
from .decorators import user_access_check


@api_view(['POST'])
def student_token(request):
    token = request.POST.get('token', None)
    if token is None:
        return Response({"message": "Please provide token"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    try:
        payload = jwt.decode(token, str(settings.NM_JWT_SECRET), algorithms=["HS256"])
        student_id = payload.get("student_id", None)
        course_id = payload.get("course_id", None)
        key = payload.get("key", None)

        get_student_user = User.objects.get(username__iexact=student_id)
        get_course = Course.objects.get(course_unique_id=course_id)
        get_temp_token = TempToken.objects.get(
            user_id=get_student_user.id,
            course_id=get_course.id,
            token=key,
            status=0
        )
        get_temp_token.status = 1
        get_temp_token.save()
        refresh = TokenObtainPairSerializer.get_token(get_student_user)
        context = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "first_name": get_student_user.first_name,
            "last_name": get_student_user.first_name,
            "email": get_student_user.email,
            "course_id": get_course.id,
        }
        return Response(context, status=status.HTTP_200_OK, content_type='application/json')

    except Exception as e:
        context = {
            "message": "Invalid",
            "error": str(e)
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


@api_view(['POST'])
def login(request):
    email = request.data.get('email', None)
    password = request.data.get('password', None)
    if email is None or password is None:
        return Response({"message": "Please provide email/ password"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    try:
        get_user = User.objects.get(email__iexact=email)
        user = authenticate(username=get_user.username, password=password)
        if user:

            refresh = TokenObtainPairSerializer.get_token(user)
            context = {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "first_name": user.first_name,
                "last_name": user.first_name,
                "email": user.email,
                "account_role": user.account_role,
            }
            return Response(context, status=status.HTTP_200_OK, content_type='application/json')
        else:
            context = {
                "message": "Please provide valid email/ password",
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    except Exception as e:
        context = {
            "message": "Please provide valid email/ password",
            "error": str(e)
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


@api_view(['POST'])
def token_refresh(request):
    refresh_key = request.POST.get('refresh', None)
    if refresh_key is None:
        return Response({"message": "Please provide refresh"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    try:
        refresh = RefreshToken(refresh_key)
        context = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        return Response(context, status=status.HTTP_200_OK, content_type='application/json')

    except Exception as e:
        context = {
            "message": "Please provide valid refresh",
            "error": str(e)
        }
        return Response(context, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.STUDENT, UserRoles.NM_USER, UserRoles.ADMIN])
def profile(request):
    try:
        user = User.objects.get(id=request.user.id)
        context = {
            "first_name": user.first_name,
            "last_name": user.first_name,
            "email": user.email,
            "account_role": user.account_role
        }
        return Response(context, status=status.HTTP_200_OK, content_type='application/json')

    except Exception as e:
        context = {
            "message": "Please provide valid email/ password",
            "error": str(e)
        }
        return Response(context, status=status.HTTP_200_OK, content_type='application/json')


