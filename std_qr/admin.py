from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(ImportExportModelAdmin):

    # Columns in admin list view
    list_display = (
        'form_title',
        'full_name',
        'college_name',
        'branch_department',
        'year_of_study',
        'email_address',
        'mobile_number',
        'preferred_learning_domain',
        'interested_in_internship',
        'interested_in_job',
        'team_name',
        'created_at',
    )

    # Filters (must be real fields)
    list_filter = (
        'year_of_study',
        'preferred_learning_domain',
        'current_skill_level',
        'interested_in_internship',
        'interested_in_job',
        'preferred_career_domain',
        'open_to_remote',
        'created_at',
    )

    # Search box
    search_fields = (
        'full_name',
        'email_address',
        'mobile_number',
        'college_name',
        'team_name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    # Admin form layout
    fieldsets = (

        ('Basic Information', {
            'fields': (
                'full_name',
                'college_name',
                'college_code',
                'branch_department',
                'year_of_study',
                'email_address',
                'mobile_number',
            )
        }),

        ('Learning Preferences', {
            'fields': (
                'preferred_learning_domain',
                'preferred_learning_domain_other',
                'preferred_mode_of_learning',
                'current_skill_level',
            ),
            'classes': ('collapse',),
        }),

        ('Internship & Job Interest', {
            'fields': (
                'interested_in_internship',
                'interested_in_job',
                'previous_internship_experience',
                'internship_company_name',
                'internship_role',
                'internship_duration',
                'internship_skills_gained',
                'prior_job_experience',
                'job_company_name',
                'job_role',
                'job_duration',
                'job_skills_gained',
            ),
            'classes': ('collapse',),
        }),

        ('Career Preferences', {
            'fields': (
                'preferred_career_domain',
                'preferred_career_domain_other',
                'availability',
                'open_to_remote',
                'resume',
            ),
            'classes': ('collapse',),
        }),

        ('Hackathon Details', {
            'fields': (
                'team_name',
                'need_mentor_support',
                'college_registration_number',
                'naan_mudhalvan_id',
                'district',
                'project_file',
            ),
            'classes': ('collapse',),
        }),

        ('Consent & Metadata', {
            'fields': (
                'communication_consent',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )

    date_hierarchy = 'created_at'
