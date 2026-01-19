from django.core.exceptions import PermissionDenied
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from django.db.models import Q
from .models import User


def user_access_check(user_roles: list = []):
    """
    Checks if the user has the required roles to access the view/ API.
    :param permission_roles:
    :param user_roles:
    :return:
    permission_roles: list of roles that are required to access the view/ API which are COLUMN's of UserRoles Model.
    user_roles: list of roles that the user value of 'account_role' in CustomUser Model.
    """

    def wrapper(view_func):
        def wrapped(request, *args, **kwargs):
            # Check if the user has authenticated or not.
            if request.user.is_authenticated:
                user_account_role_check = True
                # if permission_roles is not empty, check if the user has the required roles to access the view/ API.
                # if user_roles is not empty, check if the user has the required roles to access the view/ API.
                if user_roles:
                    user_account_role_check = User.objects.filter(account_role__in=user_roles,
                                                                        id=request.user.id).exists()
                # if the user has the required roles to access the view/ API, return the view/ API.
                if user_account_role_check:
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            else:
                raise PermissionDenied

        return wrapped

    return wrapper
