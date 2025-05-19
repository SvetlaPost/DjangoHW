from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST":
            return request.user and request.user.is_authenticated

        return obj.owner == request.user


class IsAdminWithMessage(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        raise PermissionDenied("Доступ разрешён только администраторам.")


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user




