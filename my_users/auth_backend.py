from django.contrib.auth.backends import BaseBackend
from .models import CustomUser


class PhoneAuthBackend(BaseBackend):
    def authenticate(self, request, phone_number=None):
        """ لاگین کاربران عادی بدون پسورد """
        try:
            return CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
