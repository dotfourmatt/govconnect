from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class Service(models.Model):
    """Service Model for services that a user can opt-into"""

    name = models.CharField(max_length=50)
    description = models.TextField()
    url = models.URLField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CustomAccountManager(BaseUserManager):
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

        # Create User
        email = self.normalize_email(email)
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


class GovConnectUser(AbstractBaseUser, PermissionsMixin):
    class IDType(models.TextChoices):
        """Enum for ID Types"""

        DRIVER_LICENSE = "DL", _("Driver License")
        MARINE_LICENSE_INDICATOR = "ML", _("Marine License")
        PASSPORT = "PP", _("Passport")
        BIRTH_CERTIFICATE = "BC", _("Birth Certificate")
        PROOF_OF_AGE_CARD = "POA", _("Proof of Age Card")
        PHOTO_IDENTIFICATION_CARD = "PIC", _("Photo Identification Card")

    # == Mandatory Information ==
    email = models.EmailField(_("Email Address"), unique=True)
    phone_number = models.CharField(
        _("Phone Number"), max_length=20, unique=True, null=True, blank=True
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=150)

    # == Identification Information -> Also Mandatory ==
    primary_identification = models.CharField(
        max_length=3, choices=IDType.choices, default=IDType.DRIVER_LICENSE
    )
    # Effectively The User's Password, however the user must complete a 2FA to be authenticated
    primary_identification_number = models.CharField(max_length=50, unique=True)
    # E.g. [['ID Type', 'ID Number'], ['PP', '123456789']]
    other_identities = ArrayField(
        ArrayField(models.CharField(max_length=50), size=2), null=True, blank=True
    )

    # == Other Information ==
    date_created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    # == MultiFactor Authentication ==
    # The user MUST use a type of MFA to login
    # By default, the secret question will be used for authentication
    # Secret Questions will be chosen/created by the user to provide an extra layer of security, however premade questions are provided
    secret_question = models.CharField(max_length=150)
    secret_question_answer = models.CharField(max_length=150)
    # Sends SMS one-time password
    sms_one_time_password = models.BooleanField(default=False)
    # Sends Email One-Time Password
    email_one_time_password = models.BooleanField(default=False)
    # Uses FIDO Passwordless Authentication
    passwordless_login = models.BooleanField(default=False)
    # Uses a physical security device to authenticate the user
    physical_security_authentication = models.BooleanField(default=False)

    # == Permissions ==
    is_staff = models.BooleanField(default=False)

    # == Define Custom Manager ==
    objects = CustomAccountManager()

    # == Fields Required for Account Creation ==
    USERNAME_FIELD = "primary_identification_number"
    REQUIRED_FIELDS = [
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "date_of_birth",
        "address",
        "secret_question",
        "secret_question_answer",
        "primary_identification",
    ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
