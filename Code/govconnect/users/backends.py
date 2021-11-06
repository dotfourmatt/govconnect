from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import GovConnectUser


class GovConnectUserAuthenticationBackend(ModelBackend):
    def authenticate(
        self, request, id_num=None, id_type=None, date_of_birth=None, **kwargs
    ):
        """
        Authentication method
        """
        try:
            user = GovConnectUser.objects.get(
                primary_identification=id_type,
                primary_identification_number=id_num,
                date_of_birth=date_of_birth,
            )

        except User.MultipleObjectsReturned:
            return None

        except GovConnectUser.DoesNotExist:
            return None

        if getattr(user, "is_active"):
            return user

        return None

    def get_user(self, user_id):
        try:
            return GovConnectUser.objects.get(pk=user_id)
        except GovConnectUser.DoesNotExist:
            return None
