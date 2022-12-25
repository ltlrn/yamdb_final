from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    allowed_role = 'admin'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if (
                request.user.role == self.allowed_role
                or request.user.is_superuser
            ):
                return True
        return False
