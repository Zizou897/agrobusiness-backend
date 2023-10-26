from rest_framework.permissions import BasePermission, SAFE_METHODS


class AllowOnlyCreateUpdateDelete(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in ["POST", "PUT", "PATCH", "DELETE"] and
            request.user and
            request.user.is_authenticated
        )