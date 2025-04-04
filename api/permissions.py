from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """Allow only Admin users to access"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin')

class IsRegularUser(BasePermission):
    """Allow only Regular users to access"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'user')
