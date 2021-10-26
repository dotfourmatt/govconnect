from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class AccountManager(BaseUserManager):
    def create_user(
        self,
        first_name,
        last_name,
        date_of_birth,
        email,
        primary_identification,
        primary_identification_number,
    ):
        pass


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    class IDType(models.TextChoices):
        """Enum for ID Types"""

        DRIVER_LICENCE = "DL", _("Driver License")
        MARINE_LICENCE_INDICATOR = "ML", _("Marine License")
        PASSPORT = "PP", _("Passport")
        BIRTH_CERTIFICATE = "BC", _("Birth Certificate")
        PROOF_OF_AGE_CARD = "POA", _("Proof of Age Card")
        PHOTO_IDENTIFICATION_CARD = "PIC", _("Photo Identification Card")

    # Mandatory Information
    email = models.EmailField(_("Email Address"), unique=True)
    phone_number = models.CharField(
        _("Phone Number"), max_length=20, unique=True, null=True, blank=True
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=150)
    secret_question = models.CharField(max_length=150)

    # Identification Information -> Also Mandatory
    primary_identification = models.CharField(
        max_length=3, choices=IDType.choices, default=IDType.DRIVER_LICENCE
    )
    primary_identification_number = models.CharField(max_length=50, unique=True)
    other_identities = models.ListField(
        models.CharField(max_length=3, choices=IDType.choices), null=True, blank=True
    )
    other_identity_numbers = models.ListField(max_length=50, null=True, blank=True)

    # Other Information
    date_created = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    # MultiFactor Authentication
    mfa_enabled = models.BooleanField(default=False)

    USERNAME_FIELD = "primary_identification_number"
    REQUIRED_FIELDS = [
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "date_of_birth",
        "address",
        "secret_question",
        "primary_identification",
    ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
