from django.db import models
import uuid


def get_uid():
    uid = str(uuid.uuid4())
    uid = uid[::-1]
    return uid.replace("-","")


# Create your models here.
class TempToken(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True, default=get_uid())
    status = models.IntegerField(default=0)  # 0 - new, 1, 2 - used, hard closed

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
