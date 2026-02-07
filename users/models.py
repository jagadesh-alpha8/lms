from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserRoles:
    ADMIN = 0
    STUDENT = 1
    NM_USER = 2


class User(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    """
    :account_role
    0 - admin
    1 - student
    2 - nm api
    """
    account_role = models.IntegerField(default=1)
    """
    :origin
    0 - NM
    """
    origin = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.username)

