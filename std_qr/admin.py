from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'zone')
    list_filter = ('zone',)
    search_fields = ('name',)

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'district')
    list_filter = ('district',)
    search_fields = ('name',)


@admin.register(Registration)
class RegistrationAdmin(ImportExportModelAdmin):

    # Show college name/code using methods
    list_display = (
        'form_title',
        'full_name',
        'get_college_name',
        # 'get_college_code',
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

    search_fields = (
        'full_name',
        'email_address',
        'mobile_number',
        'college__name',  # use related field
        'team_name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'full_name',
                'zone',
                'district',
                'college',  # just show the ForeignKey
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

    # Methods to display college name/code in list display
    def get_college_name(self, obj):
        return obj.college.name if obj.college else ''
    get_college_name.short_description = 'College Name'

  