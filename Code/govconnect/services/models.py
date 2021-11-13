from re import match

from django.core.exceptions import PermissionDenied, ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField

from govconnect.users.models import GovConnectUser

# Services AUS: https://www.servicesaustralia.gov.au/
# Services ACT: https://www.act.gov.au/o/services
# Services NSW: https://www.service.nsw.gov.au/services
# Services NT:  https://nt.gov.au/services
# Services QLD: https://www.qld.gov.au/services
# Services SA:  https://service.sa.gov.au/
# Services TAS: https://www.service.tas.gov.au/
# Services VIC: https://service.vic.gov.au/
# Services WA:  https://www.wa.gov.au/services

# Services are divided into state services and federal services
# Each State has its own service model
# For now, only queensland has its own unique model, since that is the only API we can access


class Service(models.Model):
    name = models.CharField(max_length=100)
    name_slug = models.SlugField(max_length=100, unique=True)
    url = models.URLField(max_length=200, unique=True)
    description = models.TextField(blank=True)


class FederalService(Service):
    pass


class StateService(Service):
    class State(models.TextChoices):
        AUSTRALIAN_CAPITAL_TERRITORY = "ACT", _("Australian Capital Territory")
        NEW_SOUTH_WALES = "NSW", _("New South Wales")
        NORTHEN_TERRITORY = "NT", _("Northern Territory")
        QUEENSLAND = "QLD", _("Queensland")
        SOUTH_AUSTRALIA = "SA", _("South Australia")
        TASMANIA = "TAS", _("Tasmania")
        VICTORIA = "VIC", _("Victoria")
        WESTERN_AUSTRALIA = "WA", _("Western Australia")

    state = models.CharField(max_length=3, choices=State.choices, default=None)

    def get_absolute_url(self):
        return reverse("service-redirect", kwargs={"state": self.state, "service-name": self.name_slug})


class AustralianCapitalTerritoryService(StateService):
    state = models.CharField(max_length=3, choices=State.choices, default=State.AUSTRALIAN_CAPITAL_TERRITORY)


class NewSouthWalesService(StateService):
    state = models.CharField(max_length=3, choices=State.choices, default=State.NEW_SOUTH_WALES)


class NorthernTerritoryService(StateService):
    state = models.CharField(max_length=3, choices=State.choices, default=State.NORTHEN_TERRITORY)


# ID Checking, they should look like: P000000
qld_id_validator = RegexValidator(r"^P\d{6}", "Interaction ID is invalid")


class QueenslandService(StateService):
    interaction_id = models.CharField(max_length=7, primary_key=True, validators=[qld_id_validator])
    type = models.CharField(max_length=100)
    type_slug = models.SlugField(max_length=100)
    category = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100)
    available = models.BooleanField(default=False)
    kiosk_friendly = models.BooleanField(default=False)
    kiosk_only = models.BooleanField(default=False)
    print_required = models.BooleanField(default=False)
    ossio = models.BooleanField(default=False)
    relevance = models.CharField(max_length=100)
    state = models.CharField(max_length=3, choices=State.choices, default=State.QUEENSLAND)


class SouthAustraliaService(StateService):
    state = models.CharField(max_length=3, choices=State.choices, default=State.SOUTH_AUSTRALIA)


class TasmaniaService(StateService):
    state = models.CharField(max_length=3, choices=State.choices, default=State.TASMANIA)


class VictoriaService(StateService):
    state = models.CharField(max_length=3, choices=State.choices, default=State.VICTORIA)


class WesternAustraliaService(StateService):
    state = models.CharField(max_length=3, choices=State.choices, default=State.WESTERN_AUSTRALIA)


class ServiceForm(models.Model):
    """
    A form for a service
    """

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    form_name = models.CharField(max_length=255, unique=True)
    # Field types are in the formart of django form Fields
    # e.g: [{"field_name": "field_type"}, {"email": "EmailField"}]
    form_fields = ArrayField(models.JSONField())

    def get_absolute_url(self):
        return reverse(
            "service_form",
            kwargs={
                "state": self.service.state,
                "service-name": self.service.name_slug,
            },
        )


class SubmittedForms(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(GovConnectUser, on_delete=models.CASCADE)
    # e.g: [{"field_name": "field_value"}]
    information = ArrayField(models.JSONField())
