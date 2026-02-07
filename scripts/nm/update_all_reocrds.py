from assessments.models import Assessment, StudentAssessment
assessments = Assessment.objects.all().order_by('serial')
assessment_count = assessments.count()
for index, assessment in enumerate(assessments):
    student_assessments = StudentAssessment.objects.filter(
        assessment_id=assessment.id
    )
    std_count = student_assessments.count()
    for index2, std in enumerate(student_assessments):
        std.api_send=True
        std.save()
        print(f"{index}: Pending({std_count-index2})")

