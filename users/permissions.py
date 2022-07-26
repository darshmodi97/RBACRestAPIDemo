from rest_framework.permissions import BasePermission

from users.models import BlackListedToken


class IsTokenValid(BasePermission):
    """
    This permission class will check whether the JWT token is valid or not.
    """

    def __init__(self):
        self.message = "Session time out you have to login again."  # setting custom message.

    def has_permission(self, request, view):
        user_id = request.user.id
        is_allowed_user = True        
        if request.auth:
            jti = request.auth.get("jti")
        else:
            return False
        try:
            is_blackListed = BlackListedToken.objects.get(user_id=user_id, jti_token=jti)
            if is_blackListed:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
