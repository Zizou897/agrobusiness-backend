from rest_framework.permissions import BasePermission, SAFE_METHODS


class AllowOnlyCreateUpdateDelete(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in ["POST", "PUT", "PATCH", "DELETE"]
            and request.user
            and request.user.is_authenticated
        )


class AllowOnlyVendor(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_vendor()
        )


class AllowOnlyVendorOnDetroy(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.method == "DELETE":
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.is_vendor()
            )
        return True


class AllowUserOnlyOnGet(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.method in [
            "PUT",
            "PATCH",
            "DELETE",
            "POST",
        ]:
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.is_vendor()
            )
        return True