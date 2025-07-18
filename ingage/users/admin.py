from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.site_header = "Ingage admin"
admin.site.site_title = "Ingage admin"


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id', 'username', 'account_role',  'email', 'origin']
    list_filter = ['account_role', 'origin']
    search_fields = ['username', 'email']


UserAdmin.fieldsets += (
    (
        'Custom fields', {
            'fields': (
                'account_role',
                'origin',)
        }
    ),
)

