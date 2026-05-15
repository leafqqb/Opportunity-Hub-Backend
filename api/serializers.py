from rest_framework import serializers

from .models import Bookmark, Opportunity


class OpportunitySerializer(serializers.ModelSerializer):
    """
    Full serializer for creating, updating, and listing opportunities.
    - posted_by shows the username (read-only).
    - status is a computed property (active / expired / inactive).
    - is_expired is a computed boolean for the frontend deadline tracker.
    """

    posted_by = serializers.CharField(source="posted_by.username", read_only=True)
    posted_by_id = serializers.IntegerField(source="posted_by.id", read_only=True)
    status = serializers.CharField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            "id",
            "title",
            "organization_name",
            "description",
            "opportunity_type",
            "category",
            "location",
            "external_url",
            "application_deadline",
            "is_paid",
            "is_urgent",
            "major",
            "responsibilities",
            "requirements",
            "benefits",
            "is_active",
            "posted_by",
            "posted_by_id",
            "status",
            "is_expired",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "posted_by",
            "posted_by_id",
            "status",
            "is_expired",
            "is_active",   # only admins toggle this
            "created_at",
            "updated_at",
        ]


class OpportunityListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for list views — fewer fields = faster responses.
    """

    posted_by = serializers.CharField(source="posted_by.username", read_only=True)
    status = serializers.CharField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            "id",
            "title",
            "organization_name",
            "opportunity_type",
            "category",
            "location",
            "application_deadline",
            "is_paid",
            "is_urgent",
            "major",
            "external_url",
            "posted_by",
            "status",
            "is_expired",
            "created_at",
        ]


class BookmarkSerializer(serializers.ModelSerializer):
    """
    - On write:  send { "opportunity_id": <int> }
    - On read:   get back full nested opportunity detail + created_at
    The user field is always set from request.user in the view, never from client input.
    """

    user = serializers.CharField(source="user.username", read_only=True)
    opportunity = OpportunityListSerializer(read_only=True)
    opportunity_id = serializers.PrimaryKeyRelatedField(
        queryset=Opportunity.objects.filter(is_active=True),
        source="opportunity",
        write_only=True,
    )

    class Meta:
        model = Bookmark
        fields = ["id", "user", "opportunity", "opportunity_id", "created_at"]
        read_only_fields = ["id", "user", "opportunity", "created_at"]