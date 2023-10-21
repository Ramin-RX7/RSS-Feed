from rest_framework.permissions import BasePermission



class IsOwner(BasePermission):
    def has_object_permission(self, request, view, user):
        print(user.id == request.user.id)
        return user.id == request.user.id
