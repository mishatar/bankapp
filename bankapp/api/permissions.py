from rest_framework import permissions
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log'
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
 
        return bool(request.user and request.user.is_staff)