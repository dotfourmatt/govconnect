from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import GovConnectUser, EnabledServices

id_choices = [
    ("", _("Select an ID type")),
    ("DL", _("Driving License")),
    ("ML", _("Marine License")),
    ("PP", _("Passport")),
    ("BC", _("Birth Certificate")),
    ("POA", _("Proof of Age Card")),
    ("PIC", _("Photo Identification Card")),
]


class GovConnectAuthenticationForm(AuthenticationForm):
    """Custom User Authentication Form for GovConnect"""

    password = None  # Remove password field from form

    id_type = forms.CharField(
        label=_("Primary Identification Type"),
        max_length=50,
        widget=forms.Select(choices=id_choices),
    )
    username = forms.CharField(
        label=_("Primary Identification Number"),
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "License No. / CRN", "autofocus": True}),
    )
    date_of_birth = forms.DateField(label=_("Date of Birth"), widget=forms.DateInput(attrs={"type": "date"}))


class GovConnect2FactorAuthenticationForm(forms.ModelForm):
    secret_question_answer = forms.CharField(
        label=_("Secret Question"),
        max_length=150,
        help_text=_("Enter the answer to your secret question"),
        widget=forms.Textarea(
            attrs={
                "autofocus": True,
                "required": True,
                "placeholder": "The answer to your secret question...",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = GovConnectUser
        fields = ("secret_question_answer",)


class UpdateGovConnectUserForm(forms.ModelForm):
    class Meta:
        model = GovConnectUser
        # The MFA items will be modified in a different view
        # since they require setup outside of the form
        # They are in this form to show their status
        fields = [
            "primary_identification",
            "primary_identification_number",
            "email",
            "phone_number",
            "street_address",
            "suburb",
            "state",
            "postcode",
            "sms_one_time_password",
            "email_one_time_password",
            "one_time_generator",
            "passwordless_login",
            "physical_security_authentication",
        ]
