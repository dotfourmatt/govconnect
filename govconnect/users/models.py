from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import GovConnectUserManager


class GovConnectUser(AbstractBaseUser, PermissionsMixin):
    class IDType(models.TextChoices):
        """Enum for ID Types"""

        DRIVER_LICENSE = "DL", _("Driver License")
        MARINE_LICENSE_INDICATOR = "ML", _("Marine License")
        PASSPORT = "PP", _("Passport")
        BIRTH_CERTIFICATE = "BC", _("Birth Certificate")
        PROOF_OF_AGE_CARD = "POA", _("Proof of Age Card")
        PHOTO_IDENTIFICATION_CARD = "PIC", _("Photo Identification Card")

    class StateOptions(models.TextChoices):
        AUSTRALIAN_CAPITAL_TERRITORY = "ACT", _("Australian Capital Territory")
        NEW_SOUTH_WALES = "NSW", _("New South Wales")
        NORTH_TERRITORY = "NT", _("North Territory")
        SOUTHERN_AUSTRALIA = "SA", _("Southern Australia")
        TASMANIA = "TAS", _("Tasmania")
        VICTORIA = "VIC", _("Victoria")
        QUEENSLAND = "QLD", _("Queensland")
        WESTERN_AUSTRALIA = "WA", _("Western Australia")

    # == Mandatory Information ==
    email = models.EmailField(_("Email Address"), unique=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    other_names = ArrayField(models.CharField(max_length=150), blank=True, null=True)
    date_of_birth = models.DateField()
    street_address = models.CharField(max_length=150)
    suburb = models.CharField(max_length=150)
    state = models.CharField(max_length=3, choices=StateOptions.choices)
    postcode = models.IntegerField()
    address = models.CharField(max_length=150)

    # == Identification Information -> Also Mandatory ==
    primary_identification = models.CharField(
        max_length=3, choices=IDType.choices, default=IDType.DRIVER_LICENSE
    )
    # Effectively The User's Password, however the user must complete a 2FA to be authenticated
    primary_identification_number = models.CharField(max_length=50, unique=True)
    # E.g. [['ID Type', 'ID Number'], ['PP', '123456789']]
    other_identities = ArrayField(ArrayField(models.CharField(max_length=50), size=2), null=True, blank=True)

    # The 'Your Data' page will show services are storing the users information, and what information they have.
    # E.g.
    #  [
    #    ["Service ID 1", "Service Full Name 1", "Service Link 1",
    #      ["The information they have 1"]
    #    ],
    #    ["Service ID 2", "Service Full Name 2", "Service Link 2",
    #      ["The information they have 2"]
    #    ]
    #  ]
    services_that_have_your_data = ArrayField(
        ArrayField(models.CharField(max_length=150)), blank=True, null=True
    )

    # == Other Information ==
    date_created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now, null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    # Password isn't needed
    password = None

    # == MultiFactor Authentication ==
    # The user MUST use a type of MFA to login
    # By default, the secret question will be used for authentication
    # Secret Questions will be chosen/created by the user to provide an extra layer of security, however premade questions are provided
    secret_question = models.CharField(max_length=150)
    # Answers will be hashed and stored in the database
    secret_question_answer = models.CharField(max_length=150)
    # Sends SMS one-time password
    sms_one_time_password = models.BooleanField(default=False)
    # Sends Email One-Time Password
    email_one_time_password = models.BooleanField(default=False)
    # Uses a One-time Password Generator
    one_time_generator = models.BooleanField(default=False)
    # Uses FIDO Passwordless Authentication
    passwordless_login = models.BooleanField(default=False)
    # Uses a physical security device to authenticate the user
    physical_security_authentication = models.BooleanField(default=False)

    # == Permissions ==
    is_staff = models.BooleanField(default=False)

    # == Define Custom Manager ==
    objects = GovConnectUserManager()

    # == Fields Required for Account Creation ==
    USERNAME_FIELD = "primary_identification_number"
    REQUIRED_FIELDS = [
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "date_of_birth",
        "street_address",
        "suburb",
        "state",
        "postcode",
        "secret_question",
        "secret_question_answer",
        "primary_identification",
    ]

    def save(self, *args, **kwargs):
        self.address = f"{self.street_address}, {self.suburb} {self.state} {self.postcode}"
        super(GovConnectUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class EnabledServices(models.Model):
    """
    The EnabledServices model contains the data for which services users have enabled
    This will determine which services are searchable by the user
    """

    user = models.ForeignKey(GovConnectUser, on_delete=models.CASCADE)
    # {"service_name": True}, {"service_name": False}, etc.
    services = models.JSONField(
        default={"Federal": {"Centrelink": False, "Child Support": False, "Medicare": False}}
    )

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}"
