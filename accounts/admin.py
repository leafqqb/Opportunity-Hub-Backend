from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "role", "company_name", "university", "is_staff"]
    list_filter = ["role", "is_staff", "is_active"]
    search_fields = ["username", "email", "company_name", "university"]

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "role",
                    "headline",
                    "bio",
                    "location",
                    "website",
                    "university",
                    "graduation_year",
                    "major",
                    "skills",
                    "company_name",
                    "industry",
                )
            },
        ),
    )