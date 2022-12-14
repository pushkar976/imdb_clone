from rest_framework import permissions


class AdminorReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
class IsOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
    
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user    #Here reviewer is coming from Review model