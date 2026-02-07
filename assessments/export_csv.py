import csv
from django.http import HttpResponse
from .models import StudentAssessment

class StudentAssessmentExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        # field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        # writer.writerow(field_names)
        headers = ["id", "assessment_name", "student_email", "total_questions_count", 'correct_answer_count', 'wrong_answer_count', 'created_at']
        writer.writerow(headers)
        for obj in queryset:
            # row = writer.writerow([getattr(obj, field) for field in field_names])
            row = writer.writerow([
                # "id",
                obj.id,
                 # "assessment_name",
                obj.assessment.name if obj.assessment_id else None,
                # "student_email",
                obj.user.email,
                obj.total_questions_count,
                obj.correct_answer_count,
                obj.wrong_answer_count,
                obj.created_at
            ])

        return response

    export_as_csv.short_description = "Export Selected"
