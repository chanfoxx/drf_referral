from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """ Права доступа для владельца. """
    message = 'Вы не являетесь владельцем профиля.'

    def has_object_permission(self, request, view, obj):
        """ Настраивает способ проверки разрешений. """
        return request.user == obj


class IsSuperUser(BasePermission):
    """ Права доступа для супер пользователя. """

    def has_permission(self, request, view):
        """ Настраивает способ проверки разрешений. """
        return request.user.is_superuser
