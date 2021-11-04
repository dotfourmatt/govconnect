from django.contrib.auth import models
from django.contrib.auth.hashers import make_password

class GovConnectUserManager(models.BaseUserManager):
    def create_user(
        self,
        email,
        phone_number,
        first_name,
        last_name,
        date_of_birth,
        address,
        secret_question,
        secret_question_answer,
        primary_identification,
        primary_identification_number,
        **other_fields,
    ):
        # Some validation
        if not email:
            raise ValueError(_("You must provide an email"))

        if not phone_number:
            raise ValueError(_("You must provide a phone number"))

        if not primary_identification:
            raise ValueError(_("You must provide a primary identification"))

        if not primary_identification_number:
            raise ValueError(_("You must provide a primary identification number"))

        # Hash Secret Question Answer
        secret_question_answer = make_password(secret_question_answer)

        email = self.normalize_email(email)
        # Create User
        user = self.model(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            address=address,
            secret_question=secret_question,
            secret_question_answer=secret_question_answer,
            primary_identification=primary_identification,
            primary_identification_number=primary_identification_number,
            **other_fields,
        )

        return user

    def create_superuser(
        self,
        email,
        phone_number,
        first_name,
        last_name,
        date_of_birth,
        address,
        secret_question,
        secret_question_answer,
        primary_identification,
        primary_identification_number,
        **other_fields,
    ):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if other_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(
            email,
            phone_number,
            first_name,
            last_name,
            date_of_birth,
            address,
            secret_question,
            secret_question_answer,
            primary_identification,
            primary_identification_number,
            **other_fields,
        )
