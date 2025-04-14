from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Anyone can view
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only owner can update/delete
        return obj.owner == request.user

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
