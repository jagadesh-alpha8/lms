from rest_framework.decorators import api_view, authentication_classes, permission_classes
from ..models import Course, CourseModule, CourseVideo, UserWatchedVideo
from rest_framework import status
from rest_framework.response import Response
import uuid

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from users.decorators import user_access_check
from users.models import UserRoles
from assessments.models import StudentAssessment


def get_uid():
    uid = str(uuid.uuid4())
    uid = uid[::-1]
    return uid.replace("-", "")[:8]


@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.ADMIN, UserRoles.STUDENT])
def course_list(request):
    # GET
    if request.method == 'GET':
        page = int(request.GET.get('page', 0))
        limit = int(request.GET.get('limit', 20))
        query = {}
        search_text = request.GET.get('search_text', None)
        if search_text:
            query['course_name__istartswith'] = search_text
        all_courses = Course.objects.filter(**query)
        data = []
        for item in all_courses[(page * limit): (page * limit) + limit]:
            temp = {
                'course_id': item.id,
                'course_unique_id': item.course_unique_id,
                'course_name': item.course_name,
                'description': item.description,
                'image': item.image.url if item.image else None,
                'status': item.status,
                'duration': item.duration,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
            }
            data.append(temp)
        context = {
            'data': data,
            'page': page,
            'limit': limit,
            'total_count': all_courses.count()
        }
        return Response(context, status=status.HTTP_200_OK)


@api_view(['POST', 'PATCH'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.ADMIN])
def course(request):
    """
    GET - get all the courses list with filter & pagination
    POST - create new course with unique course_unique_id
    PATCH - update course details except course_unique_id
    """

    # POST
    if request.method == 'POST':
        course_name = request.POST.get('course_name', None)
        description = request.POST.get('description', None)
        image = request.FILES.get('image', None)
        duration = request.POST.get('duration', None)
        if course_name is None or description is None or image is None or duration is None:
            return Response({'message': 'course_name / description / image / duration is missing'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # check_unique_id = Course.objects.filter(course_unique_id__in=course_unique_id).exists()
                new_record = Course.objects.create(
                    course_name=course_name,
                    description=description,
                    image=image,
                    duration=duration,
                    course_unique_id=get_uid()
                )
                new_record.save()
                context = {
                    'message': 'Successfully created the course',
                    'data': {
                        'course_id': new_record.id,
                        'course_unique_id': new_record.course_unique_id,
                        'course_name': new_record.course_name,
                        'description': new_record.description,
                        'image': new_record.image.url if new_record.image else None,
                        'duration': new_record.duration,
                        'status': new_record.status,
                        'created_at': new_record.created_at,
                        'updated_at': new_record.updated_at,
                    }
                }
                return Response(context, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # PATCH
    elif request.method == 'PATCH':
        course_id = request.POST.get('course_id', None)
        new_course_name = request.POST.get('course_name', None)
        new_description = request.POST.get('description', None)
        new_image = request.FILES.get('image', None)
        new_duration = request.POST.get('duration', None)
        if course_id is None:
            return Response({'message': 'course_id is missing'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                get_course = Course.objects.get(id=course_id)
                get_course.course_name = new_course_name if new_course_name is not None else get_course.course_name
                get_course.description = new_description if new_description is not None else get_course.description
                get_course.image = new_image if new_image is not None else get_course.image
                get_course.duration = new_duration if new_duration is not None else get_course.duration
                get_course.save()
                context = {
                    'message': 'Successfully updated the course',
                    'data': {
                        'course_id': get_course.id,
                        'course_unique_id': get_course.course_unique_id,
                        'course_name': get_course.course_name,
                        'description': get_course.description,
                        'image': get_course.image.url if get_course.image else None,
                        'duration': get_course.duration,
                        'status': get_course.status,
                        'created_at': get_course.created_at,
                        'updated_at': get_course.updated_at,
                    }
                }
                return Response(context, status=status.HTTP_200_OK)
            except Course.DoesNotExist:
                return Response({'message': 'Invalid course_id'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Please select any of the methods'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.ADMIN, UserRoles.STUDENT])
def course_details(request):
    course_id = int(request.GET.get('course_id', None))

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({'message': 'Course not found'}, status=status.HTTP_404_OK)
    data = []
    modules = []

    all_modules = CourseModule.objects.filter(course_id=course_id)
    for module in all_modules:

        all_videos = CourseVideo.objects.filter(course_id=course_id, course_module_id=module.id)

        videos_list = []
        for item in all_videos:
            videos_list.append({
                'assessment_id': item.assessment_id,
                'is_assessment_done': StudentAssessment.objects.filter(user_id=request.user.id, assessment_id=item.assessment_id).exists(),
                'course_video_id': item.id,
                'course_id': item.course_id,
                'course_name': item.course.course_name,
                'course_module_id': item.course_module_id,
                'course_module_name': item.course_module.module_name,
                'title': item.title,
                'y_id': item.y_id,
                'content_type': item.content_type,
                'link': item.link,
                'duration': item.duration,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
                'watched': True if UserWatchedVideo.objects.filter(course_id=course_id, video_id=item.id,
                                                                   user_id=request.user.id).count() > 0 else None,
            })

        temp = {
            'course_module_id': module.id,
            'course_id': module.course_id,
            'course_name': module.course.course_name,
            'module_name': module.module_name,
            'videos': videos_list,
        }
        modules.append(temp)

    context = {
        'course_id': course.id,
        'course_unique_id': course.course_unique_id,
        'course_name': course.course_name,
        'description': course.description,
        'image': course.image.url if course.image else None,
        'duration': course.duration,
        'status': course.status,
        'modules': modules,
    }
    return Response(context, status=status.HTTP_200_OK)

