from django.contrib import admin

from .models import Bookmark, Opportunity, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'company_name', 'university', 'location', 'created_at']
    search_fields = ['user__username', 'user__email', 'company_name', 'university']
    list_filter = ['role']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'opportunity', 'created_at']
    search_fields = ['user__username', 'opportunity__title', 'opportunity__organization_name']
    list_filter = ['created_at']


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization_name', 'opportunity_type', 'location', 'is_active', 'posted_by', 'created_at']
    search_fields = ['title', 'organization_name', 'category', 'description']
    list_filter = ['opportunity_type', 'is_active']
