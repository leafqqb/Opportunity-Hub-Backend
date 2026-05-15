from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .filters import OpportunityFilter
from .models import Bookmark, Opportunity
from .permissions import IsCompanyOnly, IsOwnerOrReadOnly, IsStudentOnly
from .serializers import (
    BookmarkSerializer,
    OpportunityListSerializer,
    OpportunitySerializer,
)


class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.filter(is_active=True).select_related('posted_by')
    serializer_class = OpportunitySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OpportunityFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return OpportunityListSerializer
        return OpportunitySerializer

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    def get_queryset(self):
        queryset = Opportunity.objects.filter(is_active=True).select_related('posted_by')
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(category__icontains=search)
                | Q(organization_name__icontains=search)
            )
        return queryset

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='mine')
    def mine(self, request):
        queryset = Opportunity.objects.filter(posted_by=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.select_related('opportunity', 'user')
    serializer_class = BookmarkSerializer
    permission_classes = [IsStudentOnly]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('opportunity')

    def perform_create(self, serializer):
        opportunity = serializer.validated_data.get('opportunity')
        if Bookmark.objects.filter(user=self.request.user, opportunity=opportunity).exists():
            raise ValidationError({'detail': 'This opportunity is already bookmarked.'})
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        bookmark = self.get_object()
        if bookmark.user != request.user:
            raise PermissionDenied('You may only remove your own bookmarks.')
        return super().destroy(request, *args, **kwargs)
