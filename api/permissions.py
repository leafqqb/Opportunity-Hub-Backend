from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = 'You must own this record to edit or delete it.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_superuser:
            return True
        owner = getattr(obj, 'posted_by', None) or getattr(obj, 'user', None)
        return owner == request.user
