from rest_framework import permissions

class IsGameParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a game to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Only allow updates if the user is one of the players
        return request.user == obj.player1 or request.user == obj.player2
