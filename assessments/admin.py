from django.contrib import admin
from .models import Assessment, AssessmentQuestion, StudentAssessment
# Register your models here.
from .export_csv import StudentAssessmentExportCsvMixin
class AssessmentQuestionInline(admin.TabularInline):
    model = AssessmentQuestion
    extra = 5


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    search_fields = ['name']
    inlines = [AssessmentQuestionInline]


@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'assessment', 'question', 'option_1', 'option_2', 'option_3', 'option_4', 'created_at', 'updated_at']
    search_fields = ['assessment__name', 'question']


@admin.register(StudentAssessment)
class StudentAssessmentAdmin(admin.ModelAdmin, StudentAssessmentExportCsvMixin):
    list_display = ['id', 'assessment_name', 'username', 'total_questions_count', 'correct_answer_count', 'wrong_answer_count', 'created_at', 'updated_at']
    search_fields = ['assessment__name', 'user__username']

    list_filter = ['assessment']
    actions = ['export_as_csv']

    def username(self, obj):
        return obj.user.username if obj.user_id else None

    def assessment_name(self, obj):
        return obj.assessment.name if obj.assessment_id else None

    def course_name(self, obj):
        return obj.course.course_name if obj.course_id else None

    def course_unique_id(self, obj):
        return obj.course.course_unique_id if obj.course_id else None
