from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookmarkViewSet, OpportunityViewSet

router = DefaultRouter()
router.register(r'opportunities', OpportunityViewSet, basename='opportunity')
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('', include('accounts.urls')),
    path('', include(router.urls)),
]
