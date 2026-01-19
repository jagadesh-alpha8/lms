from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.site_header = "Ingage admin"
admin.site.site_title = "Ingage admin"


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'account_role', 'origin')

@admin.register(User)
class UserAdmin(ImportExportModelAdmin, UserAdmin):
    list_display = ['id', 'username', 'account_role', 'email', 'origin']
    list_filter = ['account_role', 'origin']
    search_fields = ['username', 'email']

UserAdmin.fieldsets += ( ( 'Custom fields', { 'fields': ( 'account_role', 'origin',) } ), )