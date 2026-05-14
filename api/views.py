from django.contrib.auth import logout
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView

from .models import Opportunity, Profile
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    LoginSerializer,
    OpportunitySerializer,
    ProfileSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.auth:
            request.auth.delete()
        logout(request)
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ProfileDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return self.request.user.profile

    def delete(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.delete()
        return Response({'detail': 'Account and profile deleted.'}, status=status.HTTP_204_NO_CONTENT)


class ProfilePublicView(RetrieveAPIView):
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'
    permission_classes = [AllowAny]


class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.filter(is_active=True).select_related('posted_by')
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    def get_queryset(self):
        queryset = Opportunity.objects.filter(is_active=True).select_related('posted_by')
        category = self.request.query_params.get('category')
        location = self.request.query_params.get('location')
        opportunity_type = self.request.query_params.get('type')
        organization = self.request.query_params.get('organization')
        search = self.request.query_params.get('search')

        if category:
            queryset = queryset.filter(category__icontains=category)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if opportunity_type:
            queryset = queryset.filter(opportunity_type__iexact=opportunity_type)
        if organization:
            queryset = queryset.filter(organization_name__icontains=organization)
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
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        if self.action in ['create']:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='mine')
    def mine(self, request):
        queryset = Opportunity.objects.filter(posted_by=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
