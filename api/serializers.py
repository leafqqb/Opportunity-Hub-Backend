from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueTogetherValidator

from .models import Bookmark, Opportunity, Profile

User = get_user_model()


class OpportunitySerializer(serializers.ModelSerializer):
    posted_by = serializers.CharField(source='posted_by.username', read_only=True)
    posted_by_id = serializers.IntegerField(source='posted_by.id', read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            'id',
            'title',
            'organization_name',
            'description',
            'opportunity_type',
            'category',
            'location',
            'external_url',
            'application_deadline',
            'is_active',
            'posted_by',
            'posted_by_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['posted_by', 'posted_by_id', 'created_at', 'updated_at']


class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    opportunity = OpportunitySerializer(read_only=True)
    opportunity_id = serializers.PrimaryKeyRelatedField(
        queryset=Opportunity.objects.filter(is_active=True),
        source='opportunity',
        write_only=True,
    )

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'opportunity', 'opportunity_id', 'created_at']
        read_only_fields = ['id', 'user', 'opportunity', 'created_at']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            attrs['user'] = request.user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'email',
            'role',
            'headline',
            'bio',
            'location',
            'website',
            'company_name',
            'university',
            'graduation_year',
            'skills',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['username', 'email', 'created_at', 'updated_at']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES)
    headline = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    location = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    website = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    company_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    university = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    graduation_year = serializers.IntegerField(required=False, allow_null=True)
    skills = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        if attrs['role'] == Profile.COMPANY and not attrs.get('company_name'):
            raise serializers.ValidationError({'company_name': 'Company accounts should include a company name.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        profile_data = {
            'role': role,
            'headline': validated_data.pop('headline', ''),
            'bio': validated_data.pop('bio', ''),
            'location': validated_data.pop('location', ''),
            'website': validated_data.pop('website', ''),
            'company_name': validated_data.pop('company_name', ''),
            'university': validated_data.pop('university', ''),
            'graduation_year': validated_data.pop('graduation_year', None),
            'skills': validated_data.pop('skills', ''),
        }
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username') or ''
        email = attrs.get('email') or ''
        password = attrs.get('password')
        if not password:
            raise serializers.ValidationError('Password is required.')

        user = None
        if email and not username:
            try:
                user_obj = User.objects.get(email__iexact=email)
                username = user_obj.username
            except User.DoesNotExist:
                raise serializers.ValidationError('Unable to log in with provided credentials.')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
