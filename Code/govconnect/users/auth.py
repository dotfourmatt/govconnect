from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import GovConnectUser


class GovConnectUserAuthenticationBackend(ModelBackend):
    def authenticate(
        self, request, id_type=None, id_num=None, date_of_birth=None, **kwargs
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
            # Authenticate with Secret Question
            """
                if check_password(secret_question, user.secret_question):
                    return user
                else:
                    return None
            """
            return user

        except GovConnectUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return GovConnectUser.objects.get(pk=user_id)
        except GovConnectUser.DoesNotExist:
            return None
