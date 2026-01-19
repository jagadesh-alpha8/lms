from django.db import IntegrityError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import CourseVideo

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from users.decorators import user_access_check
from users.models import UserRoles


@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.ADMIN])
def course_video_list(request):
    # GET
    if request.method == 'GET':
        page = int(request.GET.get('page', 0))
        limit = int(request.GET.get('limit', 20))
        query = {}
        course_name = request.GET.get('course_name', None)
        module_name = request.GET.get('module_name', None)
        if course_name:
            query['course__course_name__istartswith'] = course_name
        if module_name:
            query['course_module__module_name__istartswith'] = module_name
        all_course_video = CourseVideo.objects.filter(**query)
        data = []
        for item in all_course_video[(page * limit): (page * limit) + limit]:
            temp = {
                'course_video_id': item.id,
                'course_id': item.course_id,
                'course_name': item.course.course_name,
                'course_module_id': item.course_module_id,
                'course_module_name': item.course_module.module_name,
                'title': item.title,
                'y_id': item.y_id,
                'duration': item.duration,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
            }
            data.append(temp)
        context = {
            'data': data,
            'page': page,
            'limit': limit,
            'total_count': all_course_video.count()
        }
        return Response(context, status=status.HTTP_200_OK)


@api_view(['POST', 'PATCH'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.ADMIN])
def course_video(request):
    """
    GET - get all the course_video list with filter & pagination
    POST - create new course_video
    PATCH - update course_video details
    """
    # POST
    if request.method == 'POST':
        course_id = request.POST.get('course_id', None)
        course_module_id = request.POST.get('course_module_id', None)
        title = request.POST.get('title', None)
        y_id = request.POST.get('y_id', None)
        duration = request.POST.get('duration', None)
        if course_id is None or course_module_id is None or title is None or y_id is None or duration is None:
            return Response({'message': 'course_id / course_module_id / title / y_id / duration is missing'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                new_record = CourseVideo.objects.create(
                    course_id=course_id,
                    course_module_id=course_module_id,
                    title=title,
                    y_id=y_id,
                    duration=duration
                )
                new_record.save()
                context = {
                    'message': 'Successfully created the course video',
                    'data': {
                        'course_video_id': new_record.id,
                        'course_id': new_record.course_id,
                        'course_name': new_record.course.course_name,
                        'course_module_id': new_record.course_module_id,
                        'course_module_name': new_record.course_module.module_name,
                        'title': new_record.title,
                        'y_id': new_record.y_id,
                        'duration': new_record.duration,
                        'created_at': new_record.created_at,
                        'updated_at': new_record.updated_at,
                    }
                }
                return Response(context, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({'message': 'Invalid course_id / course_module_id'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # PATCH
    elif request.method == 'PATCH':
        course_video_id = request.POST.get('course_video_id', None)
        new_course_id = request.POST.get('course_id', None)
        new_course_module_id = request.POST.get('course_module_id', None)
        new_title = request.POST.get('title', None)
        new_y_id = request.POST.get('y_id', None)
        new_duration = request.POST.get('duration', None)
        if course_video_id is None:
            return Response({'message': 'course_video_id is missing'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                get_course_video = CourseVideo.objects.get(id=course_video_id)
                get_course_video.course_id = new_course_id if new_course_id is not None else get_course_video.course_id
                get_course_video.course_module_id = new_course_module_id if new_course_module_id is not None else get_course_video.course_module_id
                get_course_video.title = new_title if new_title is not None else get_course_video.title
                get_course_video.y_id = new_y_id if new_y_id is not None else get_course_video.y_id
                get_course_video.duration = new_duration if new_duration is not None else get_course_video.duration
                get_course_video.save()
                context = {
                    'message': 'Successfully updated the course video',
                    'data': {
                        'course_video_id': get_course_video.id,
                        'course_id': get_course_video.course_id,
                        'course_name': get_course_video.course.course_name,
                        'course_module_id': get_course_video.course_module_id,
                        'course_module_name': get_course_video.course_module.module_name,
                        'title': get_course_video.title,
                        'y_id': get_course_video.y_id,
                        'duration': get_course_video.duration,
                        'created_at': get_course_video.created_at,
                        'updated_at': get_course_video.updated_at,
                    }
                }
                return Response(context, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({'message': 'Invalid course_id / course_module_id'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Please select any of the methods'}, status=status.HTTP_200_OK)
