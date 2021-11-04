from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class GovConnectAuthenticationForm(AuthenticationForm):
    """Custom User Authentication Form for GovConnect"""

    password = None  # Remove password field from form

    id_type = forms.CharField(
        label=_("Primary Identification Type"),
        max_length=50,
        widget=forms.Select(choices=[("DL", _("Driver's License"))]),
    )
    username = forms.CharField(
        label=_("Primary Identification Number"),
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "License No. / CRN", "autofocus": True}
        ),
    )
    date_of_birth = forms.DateField(
        label=_("Date of Birth"), widget=forms.DateInput(attrs={"type": "date"})
    )
