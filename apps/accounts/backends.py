from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .models import User


class UserAuthenticationBackend(ModelBackend):

    def authenticate(email, password, organization):
        try:
            user = User.objects.get(email__iexact=email, organization=organization)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            User().set_password(password)
