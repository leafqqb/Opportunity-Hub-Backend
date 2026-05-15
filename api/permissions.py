from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission.
    - Safe methods (GET, HEAD, OPTIONS) → allowed for everyone.
    - Write methods → only the object owner or a superuser.
    Works for both Opportunity (posted_by) and Bookmark (user).
    """

    message = "You must be the owner of this record to edit or delete it."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_superuser:
            return True
        # Support both Opportunity.posted_by and Bookmark.user
        owner = getattr(obj, "posted_by", None) or getattr(obj, "user", None)
        return owner == request.user


class IsStudentOnly(BasePermission):
    """Only authenticated users with role='student' may proceed."""

    message = "Only student accounts can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_student()
        )


class IsCompanyOnly(BasePermission):
    """Only authenticated users with role='company' may proceed."""

    message = "Only company accounts can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_company()
        )
