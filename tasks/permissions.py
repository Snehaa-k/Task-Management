from rest_framework.permissions import BasePermission

class IsSuperAdminOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or getattr(request.user, 'role', None) == 'admin')

class IsSuperAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if getattr(request.user, 'role', None) == 'admin' and hasattr(obj, 'assigned_to'):
            return getattr(obj.assigned_to, 'admin', None) == request.user
        return getattr(obj, 'assigned_to', None) == request.user
