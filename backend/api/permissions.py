from rest_framework import permissions

class IsAdminOrEventOrganizers(permissions.DjangoModelPermissions):
    message = 'role anda tidak cukup'
    def has_permission(self,request,view):
        print(request)
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'event_organizer' or True


class IsAdminOrOwner(permissions.BasePermission):
    message = 'role anda tidak cukup'
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True
        return request.user.role == 'administrator' or request.user == obj.organizer