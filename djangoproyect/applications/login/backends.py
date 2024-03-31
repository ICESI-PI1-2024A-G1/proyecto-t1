from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class IDBackend(ModelBackend):
    """
    Custom authentication backend for authenticating users by ID.
    """

    def authenticate(self, request, id=None, password=None, **kwargs):
        """Authenticate a user by ID and password.

        Args:
            request: HttpRequest object.
            id (str): User ID to authenticate.
            password (str): User password to authenticate.

        Returns:
            User object: Authenticated user if successful; else, returns None.
        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(id=id)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        """Retrieve a user by ID.

        Args:
            user_id (str): User ID to retrieve.

        Returns:
            User object: User if found; else, returns None.
        """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
