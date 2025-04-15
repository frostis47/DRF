from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Является ли пользователь владельцем объекта?
    """
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsUserProfile(BasePermission):
    """
    Является ли это профиль текущего пользователя?
    """
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id