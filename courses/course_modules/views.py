from django.db import IntegrityError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import CourseModule

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from users.decorators import user_access_check
from users.models import UserRoles


@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.ADMIN, UserRoles.STUDENT])
def course_module_list(request):
    # GET
    if request.method == 'GET':
        page = int(request.GET.get('page', 0))
        limit = int(request.GET.get('limit', 20))
        query = {}
        search_text = request.GET.get('search_text', None)
        if search_text:
            query['course__course_name__istartswith'] = search_text
        all_course_modules = CourseModule.objects.filter(**query)
        data = []
        for item in all_course_modules[(page * limit): (page * limit) + limit]:
            temp = {
                'course_module_id': item.id,
                'course_id': item.course_id,
                'course_name': item.course.course_name,
                'module_name': item.module_name,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
            }
            data.append(temp)
        context = {
            'data': data,
            'page': page,
            'limit': limit,
            'total_count': all_course_modules.count()
        }
        return Response(context, status=status.HTTP_200_OK)


@api_view(['POST', 'PATCH'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@user_access_check(user_roles=[UserRoles.ADMIN])
def course_module(request):
    """
    GET - get all the course_modules list with filter & pagination
    POST - create new course_module
    PATCH - update course_module details
    """
    # POST
    if request.method == 'POST':
        course_id = request.POST.get('course_id', None)
        module_name = request.POST.get('module_name', None)
        if course_id is None or module_name is None:
            return Response({'message': 'course_id / module_name is missing'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                new_record = CourseModule.objects.create(
                    course_id=course_id,
                    module_name=module_name
                )
                new_record.save()
                context = {
                    'message': 'Successfully created the course module',
                    'data': {
                        'course_module_id': new_record.id,
                        'course_id': new_record.course_id,
                        'course_name': new_record.course.course_name,
                        'module_name': new_record.module_name,
                        'created_at': new_record.created_at,
                        'updated_at': new_record.updated_at,
                    }
                }
                return Response(context, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({'message': 'Invalid course_id'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # PATCH
    elif request.method == 'PATCH':
        course_module_id = request.POST.get('course_module_id', None)
        new_course_id = request.POST.get('course_id', None)
        new_module_name = request.POST.get('module_name', None)
        if course_module_id is None:
            return Response({'message': 'course_module_id is missing'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                get_course_module = CourseModule.objects.get(id=course_module_id)
                get_course_module.course_id = new_course_id if new_course_id is not None else get_course_module.course_id
                get_course_module.module_name = new_module_name if new_module_name is not None else get_course_module.module_name
                get_course_module.save()
                context = {
                    'message': 'Successfully updated the course module',
                    'data': {
                        'course_module_id': get_course_module.id,
                        'course_id': get_course_module.course_id,
                        'course_name': get_course_module.course.course_name,
                        'module_name': get_course_module.module_name,
                        'created_at': get_course_module.created_at,
                        'updated_at': get_course_module.updated_at,
                    }
                }
                return Response(context, status=status.HTTP_200_OK)
            except CourseModule.DoesNotExist:
                return Response({'message': 'Invalid course_module_id'}, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError:
                return Response({'message': 'Invalid course_id'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Please select any of the methods'}, status=status.HTTP_200_OK)
