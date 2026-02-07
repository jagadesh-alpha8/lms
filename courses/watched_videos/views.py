from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from users.decorators import user_access_check
from users.models import UserRoles
from rest_framework import status
from rest_framework.response import Response
from ..models import CourseModule, UserWatchedVideo, Course, CourseVideo, Subscription


@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.STUDENT, UserRoles.ADMIN])
def update_course_watched_video(request):
    course_id = request.POST.get('course_id', None)
    course_video_id = request.POST.get('course_video_id', None)

    if course_id is None or course_video_id is None:
        return Response({'message': 'Please provide course_id/ course_video_id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        get_course = Course.objects.get(id=course_id)
        get_subscription = Subscription.objects.get(
            course_id=course_id,
            user_id=request.user.id
        )
        get_course_video = CourseVideo.objects.get(id=course_video_id)
        try:

            get_user_watched_video = UserWatchedVideo.objects.get(video_id=course_video_id, user_id=request.user.id)
            return Response({'message': 'Already updated'}, status=status.HTTP_400_BAD_REQUEST)
        except UserWatchedVideo.DoesNotExist:
            get_user_watched_video = UserWatchedVideo.objects.create(
                course_id=get_course.id,
                video_id=get_course_video.id,
                user_id=request.user.id
            )
            return Response({'message': 'updated successfully'}, status=status.HTTP_200_OK)
    except Course.DoesNotExist:
        return Response({'message': 'Course not found'}, status=status.HTTP_200_OK)

    except CourseVideo.DoesNotExist:
        return Response({'message': 'Course Video not found'}, status=status.HTTP_200_OK)

    except Subscription.DoesNotExist:
        return Response({'message': 'Please subscribe the course'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'message': 'Course not found', "error": str(e)}, status=status.HTTP_200_OK)






