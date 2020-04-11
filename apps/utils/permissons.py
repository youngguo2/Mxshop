__author__ = 'Yuxiang'

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    只有owner才有权限删除收藏记录
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.
        return obj.user == request.user