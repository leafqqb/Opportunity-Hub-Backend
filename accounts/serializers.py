from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    """Read-only public view of a user — safe to expose to anyone."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
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
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Used for GET /auth/me/ and GET|PATCH /profiles/me/.
    Exposes email (private — only for the owner).
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
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
        ]
        read_only_fields = ["id", "username", "email", "role"]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    # Optional profile fields
    headline = serializers.CharField(required=False, allow_blank=True, default="")
    bio = serializers.CharField(required=False, allow_blank=True, default="")
    location = serializers.CharField(required=False, allow_blank=True, default="")
    website = serializers.URLField(required=False, allow_blank=True, default="")

    # Student fields
    university = serializers.CharField(required=False, allow_blank=True, default="")
    graduation_year = serializers.IntegerField(required=False, allow_null=True, default=None)
    major = serializers.CharField(required=False, allow_blank=True, default="")
    skills = serializers.CharField(required=False, allow_blank=True, default="")

    # Company fields
    company_name = serializers.CharField(required=False, allow_blank=True, default="")
    industry = serializers.CharField(required=False, allow_blank=True, default="")

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, attrs):
        if attrs["role"] == User.COMPANY and not attrs.get("company_name"):
            raise serializers.ValidationError(
                {"company_name": "Company accounts must include a company name."}
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
    
    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True, default="")
    email = serializers.EmailField(required=False, allow_blank=True, default="")
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username", "").strip()
        email = attrs.get("email", "").strip()
        password = attrs.get("password")

        if not password:
            raise serializers.ValidationError({"password": "Password is required."})
        if not username and not email:
            raise serializers.ValidationError(
                "Provide either a username or an email address."
            )

        # Resolve email → username
        if email and not username:
            try:
                user_obj = User.objects.get(email__iexact=email)
                username = user_obj.username
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "Unable to log in with the provided credentials."
                )

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                "Unable to log in with the provided credentials."
            )
        if not user.is_active:
            raise serializers.ValidationError("This account has been disabled.")

        attrs["user"] = user
        return attrs


class MinimalUserSerializer(serializers.ModelSerializer):
    """Tiny representation embedded in token responses."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]