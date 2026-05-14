from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BookmarkViewSet,
    CurrentUserView,
    LoginView,
    LogoutView,
    OpportunityViewSet,
    ProfileDetailView,
    ProfilePublicView,
    RegisterView,
)

router = DefaultRouter()
router.register(r'opportunities', OpportunityViewSet, basename='opportunity')
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/me/', CurrentUserView.as_view(), name='auth-me'),
    path('profiles/me/', ProfileDetailView.as_view(), name='profile-me'),
    path('profiles/<str:username>/', ProfilePublicView.as_view(), name='profile-public'),
    path('', include(router.urls)),
]
