from django.contrib.auth import get_user_model, logout
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    LoginSerializer,
    MinimalUserSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserPublicSerializer,
)

User = get_user_model()


class RegisterView(APIView):
    """
    POST /api/auth/register/
    Creates a new user account and returns a token immediately.
    No extra profile object — user IS the profile (AbstractUser).
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response(
            {
                "token": token.key,
                "user": MinimalUserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    POST /api/auth/login/
    Accepts username OR email + password. Returns token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": MinimalUserSerializer(user).data,
            }
        )


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Deletes the user's token, invalidating all active sessions.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.auth:
            request.auth.delete()
        logout(request)
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """
    GET /api/auth/me/
    Returns full profile of the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class ProfileMeView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/profiles/me/  — read own profile
    PATCH  /api/profiles/me/  — update own profile
    DELETE /api/profiles/me/  — permanently delete account
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.delete()
        return Response(
            {"detail": "Account deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProfilePublicView(generics.RetrieveAPIView):
    """
    GET /api/profiles/<username>/
    Public read-only view. No email exposed.
    """

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserPublicSerializer
    lookup_field = "username"
    permission_classes = [AllowAny]