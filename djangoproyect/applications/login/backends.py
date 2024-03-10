from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class IDBackend(ModelBackend):
    def authenticate(self, request, id=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(id=id)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None