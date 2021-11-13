from django import forms
from models import (
    StateService,
    AustralianCapitalTerritoryService,
    NewSouthWalesService,
    NorthernTerritoryService,
    QueenslandService,
    SouthAustraliaService,
    TasmaniaService,
    VictoriaService,
    WesternAustraliaService,
)

# All services will have their own form
# Since we only know the fields of queensland services, that is why it is the only one

class AddQueenslandServiceForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    url = forms.URLField(max_length=200, required=True)
    description = forms.TextArea(required=False)

    interaction_id = forms.CharField(required=True)
    type = forms.CharField(max_length=100, required=True)
    category = forms.CharField(max_length=100, required=True)
    available = forms.BooleanField(required=True)
    kiosk_friendly = forms.BooleanField(required=True)
    kiosk_only = forms.BooleanField(required=True)
    print_required = forms.BooleanField(required=True)
    ossio = forms.BooleanField(required=True)
    relevance = forms.CharField(max_length=100, required=True)

    class Meta:
        model = StateService
