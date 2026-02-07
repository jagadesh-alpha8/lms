from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(ImportExportModelAdmin):
    list_display = [
        'college_name', 
        'branch_of_study', 
        'current_year',
        'interested_in_course',
        'interested_in_hackathon',
        'participant_name',
        'created_at'
    ]
    
    list_filter = [
        'interested_in_course',
        'interested_in_hackathon',
        'current_year',
        'preferred_course_domain',
        'interested_in_opportunities',
        'created_at'
    ]
    
    search_fields = [
        'college_name',
        'branch_of_study',
        'participant_name',
        'participant_email',
        'team_name'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('college_name', 'branch_of_study', 'current_year')
        }),
        ('Course Registration', {
            'fields': (
                'interested_in_course',
                'preferred_course_domain',
                'preferred_learning_mode',
                'current_skill_level'
            ),
            'classes': ('collapse',)
        }),
        ('Internship Experience', {
            'fields': (
                'has_previous_internship',
                'internship_duration',
                'internship_roles',
                'internship_skills_gained',
                'currently_doing_internship',
                'current_internship_company',
                'current_internship_role',
                'current_internship_duration'
            ),
            'classes': ('collapse',)
        }),
        ('Job Experience', {
            'fields': (
                'has_previous_job',
                'job_duration',
                'job_roles',
                'job_skills_gained',
                'currently_employed',
                'current_job_company',
                'current_job_role',
                'current_job_duration'
            ),
            'classes': ('collapse',)
        }),
        ('Opportunity Preferences', {
            'fields': (
                'interested_in_opportunities',
                'preferred_role',
                'availability',
                'open_to_remote',
                'resume'
            ),
            'classes': ('collapse',)
        }),
        ('Hackathon Registration', {
            'fields': (
                'interested_in_hackathon',
                'has_hackathon_experience',
                'preferred_hackathon_mode',
                'participant_name',
                'participant_email',
                'team_preference',
                'team_name',
                'participant_mobile',
                'consent'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'created_at'