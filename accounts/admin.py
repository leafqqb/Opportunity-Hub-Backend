from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "username", "email", "role", "company_name",
        "university", "major", "is_active", "is_staff", "date_joined"
    ]
    list_filter = ["role", "is_staff", "is_active"]
    search_fields = ["username", "email", "company_name", "university"]
    ordering = ["-date_joined"]
    readonly_fields = ["date_joined", "last_login"]

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role", {
            "fields": ("role",)
        }),
        ("Shared Profile", {
            "fields": ("headline", "bio", "location", "website")
        }),
        ("Student Fields", {
            "fields": ("university", "graduation_year", "major", "skills"),
            "classes": ("collapse",),
        }),
        ("Company Fields", {
            "fields": ("company_name", "industry"),
            "classes": ("collapse",),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Role", {
            "fields": ("role",)
        }),
        ("Shared Profile", {
            "fields": ("headline", "bio", "location", "website")
        }),
        ("Student Fields", {
            "fields": ("university", "graduation_year", "major", "skills"),
            "classes": ("collapse",),
        }),
        ("Company Fields", {
            "fields": ("company_name", "industry"),
            "classes": ("collapse",),
        }),
    )