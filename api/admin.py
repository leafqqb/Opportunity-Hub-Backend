from django.contrib import admin
from django.utils.html import format_html
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin
from .models import Bookmark, Opportunity

TokenAdmin.raw_id_fields = ["user"]
admin.site.register(Token, TokenAdmin)


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = [
        "title", "organization_name", "opportunity_type",
        "category", "location", "posted_by", "is_paid",
        "is_urgent", "is_active", "status_badge",
        "application_deadline", "created_at"
    ]
    list_filter = ["opportunity_type", "is_active", "is_paid", "is_urgent"]
    search_fields = ["title", "organization_name", "category", "description", "posted_by__username"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at", "posted_by"]
    list_editable = ["is_active", "is_urgent"]
    date_hierarchy = "created_at"

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "organization_name", "opportunity_type", "category", "location", "external_url")
        }),
        ("Details", {
            "fields": ("description", "responsibilities", "requirements", "benefits")
        }),
        ("Targeting", {
            "fields": ("major", "is_paid", "is_urgent", "application_deadline")
        }),
        ("Status & Meta", {
            "fields": ("is_active", "posted_by", "created_at", "updated_at")
        }),
    )

    def status_badge(self, obj):
        colors = {"active": "green", "expired": "orange", "inactive": "red"}
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, "gray"),
            obj.status.upper()
        )
    status_badge.short_description = "Status"


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["user", "opportunity_title", "opportunity_type", "opportunity_deadline", "created_at"]
    list_filter = ["opportunity__opportunity_type", "created_at"]
    search_fields = ["user__username", "user__email", "opportunity__title", "opportunity__organization_name"]
    ordering = ["-created_at"]
    readonly_fields = ["user", "opportunity", "created_at"]

    def opportunity_title(self, obj):
        return obj.opportunity.title
    opportunity_title.short_description = "Opportunity"

    def opportunity_type(self, obj):
        return obj.opportunity.opportunity_type
    opportunity_type.short_description = "Type"

    def opportunity_deadline(self, obj):
        return obj.opportunity.application_deadline
    opportunity_deadline.short_description = "Deadline"