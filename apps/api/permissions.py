import typing as ty

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and obj.author == request.user


def is_author_builder(author_property: str) -> ty.Type[permissions.BasePermission]:
    class IsAuthor(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            return request.user.is_authenticated and getattr(obj, author_property, None) == request.user

    return IsAuthor
