from rest_framework import permissions



class IsAdminOrEventOrganizers(permissions.DjangoModelPermissions):
    message = "Insufficient role permissions."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['event_organizer', 'administrator']


class IsCustomerOrAdmin(permissions.BasePermission):
    message = 'Insufficient role permissions. Only administrators are allowed.'
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return super().has_object_permission(request, view, obj) or request.user.role == 'administrator'

class IsAdminOrOwner(permissions.BasePermission):
    message = "Insufficient role permissions."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'administrator' or request.user == obj.organizer

class IsAdministrator(permissions.DjangoModelPermissions):
    message = "Insufficient role permissions. Only administrators are allowed."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'administrator'
