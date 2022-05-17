from rest_framework import permissions

class TweetPermission(permissions.BasePermission):
    # permission for authenticated user for 
    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'post']:
            return bool(request.user.is_authenticated)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return obj.author == request.user or request.user.is_staff
        return True
