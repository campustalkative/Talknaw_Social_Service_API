from rest_framework import permissions
from social.models import Post, Comment


class IsAuthenticated(permissions.BasePermission):
    message = "cannot touch"
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return bool(request.user_id)

    def has_object_permission(self, request, view, obj):
        if  request.method not in permissions.SAFE_METHODS:

            if isinstance(obj, Post) or isinstance(obj, Comment):
                
                return bool(request.user_id and (obj.profile.user_id == request.user_id))
        
        return bool(request.user_id)
        
            
            
        