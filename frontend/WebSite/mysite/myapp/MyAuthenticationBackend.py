from django.contrib.auth.models import update_last_login, user_logged_in
from models import *

class MyUserBackend(object):
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(login=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

        return user
