import django_filters

from .models import Opportunity


class OpportunityFilter(django_filters.FilterSet):
    """
    Allows the frontend to filter opportunities via query params:

        GET /api/opportunities/?type=internship
        GET /api/opportunities/?location=Riyadh&is_paid=true
        GET /api/opportunities/?deadline_before=2026-06-01
        GET /api/opportunities/?deadline_after=2026-01-01
        GET /api/opportunities/?major=Computer+Science
    """

    type = django_filters.CharFilter(
        field_name="opportunity_type", lookup_expr="iexact"
    )
    location = django_filters.CharFilter(
        field_name="location", lookup_expr="icontains"
    )
    organization = django_filters.CharFilter(
        field_name="organization_name", lookup_expr="icontains"
    )
    category = django_filters.CharFilter(
        field_name="category", lookup_expr="icontains"
    )
    major = django_filters.CharFilter(
        field_name="major", lookup_expr="icontains"
    )
    is_paid = django_filters.BooleanFilter(field_name="is_paid")
    is_urgent = django_filters.BooleanFilter(field_name="is_urgent")
    deadline_before = django_filters.DateFilter(
        field_name="application_deadline", lookup_expr="lte"
    )
    deadline_after = django_filters.DateFilter(
        field_name="application_deadline", lookup_expr="gte"
    )

    class Meta:
        model = Opportunity
        fields = [
            "type",
            "location",
            "organization",
            "category",
            "major",
            "is_paid",
            "is_urgent",
            "deadline_before",
            "deadline_after",
        ]