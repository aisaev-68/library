from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Разрешить доступ к методам GET, HEAD, OPTIONS
        return request.user and (
                    request.user.is_staff or request.user.is_superuser)  # Разрешить только админам и суперпользователям доступ к методам POST, PUT, DELETE
