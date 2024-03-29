from rest_framework import permissions


class IsAdminIsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Разрешает анонимному пользователю только безопасные запросы.
    Право на осуществление остальных запросов предоставляется
    админу или суперпользователю.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_staff
                or request.user.is_superuser
            )
        )


class IsSuperUserOrIsAdminOnly(permissions.BasePermission):
    """
    Предоставляет права на осуществление запросов
    только суперпользователю, админу или
    аутентифицированному пользователю с ролью admin.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.is_staff
            or request.user.is_admin
        )


class AnonimReadOnly(permissions.BasePermission):
    """Разрешает анонимному пользователю только безопасные запросы."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsSuperUserIsAdminIsModeratorIsAuthor(permissions.BasePermission):
    """
    Разрешает анонимному пользователю только безопасные запросы.
    Доступ к запросам PATCH и DELETE предоставляется только
    суперпользователю, админу, аутентифицированным пользователям
    с ролью admin или moderator, а также автору объекта.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_staff
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
