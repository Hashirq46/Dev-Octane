from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_candidate', 'is_recruiter', 'is_verified_recruiter', 'is_staff', 'is_active')
    list_filter = ('is_candidate', 'is_recruiter', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Roles', {'fields': ('is_candidate', 'is_recruiter')}),
    )
