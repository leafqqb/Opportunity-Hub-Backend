from django.urls import path

from .views import (
    CurrentUserView,
    LoginView,
    LogoutView,
    ProfileMeView,
    ProfilePublicView,
    RegisterView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("auth/me/", CurrentUserView.as_view(), name="auth-me"),
    path("profiles/me/", ProfileMeView.as_view(), name="profile-me"),
    path("profiles/<str:username>/", ProfilePublicView.as_view(), name="profile-public"),
]