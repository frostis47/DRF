from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Является ли пользователь владельцем объекта?
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsUserProfile(BasePermission):
    """
    Является ли это профиль текущего пользователя?
    """
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id
