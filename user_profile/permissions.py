from rest_framework import permissions
from rest_framework.permissions import IsAdminUser


class IsLoggedIn(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
