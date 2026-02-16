from rest_framework import serializers
from .models import Registration

class RegistrationFullSerializer(serializers.ModelSerializer):
    zone = serializers.CharField(source='zone.name', read_only=True)
    district = serializers.CharField(source='district.name', read_only=True)
    college = serializers.CharField(source='college.name', read_only=True)

    resume = serializers.SerializerMethodField()
    project_file = serializers.SerializerMethodField()

    class Meta:
        model = Registration
        fields = "__all__"

    def get_resume(self, obj):
        request = self.context.get("request")
        if obj.resume:
            return request.build_absolute_uri(obj.resume.url)
        return None

    def get_project_file(self, obj):
        request = self.context.get("request")
        if obj.project_file:
            return request.build_absolute_uri(obj.project_file.url)
        return None
