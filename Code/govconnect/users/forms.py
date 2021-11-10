from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import GovConnectUser


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
