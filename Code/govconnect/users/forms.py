from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    id_type = forms.CharField(
        max_length=10, widget=forms.Select(choices=[("DL", _("Driver's License"))])
    )
    primary_id_no = forms.CharField(label="Primary ID No.", max_length=20)
    date_of_birth = forms.DateField(
        label="Date of Birth", widget=forms.DateInput(attrs={"type": "date"})
    )
