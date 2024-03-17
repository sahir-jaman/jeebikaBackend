from rest_framework.permissions import BasePermission

from common.choices import UserType


class IsEmployeeUser(BasePermission):
    """
    Custom permission to only allow employee users.
    """

    def has_permission(self, request, view):
        return request.user.type == UserType.EMPLOYER
