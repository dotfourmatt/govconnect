from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ViewDoesNotExist
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import MultipleObjectMixin

from .models import (
    Service,
    FederalService,
    StateService,
    AustralianCapitalTerritoryService,
    NewSouthWalesService,
    NorthernTerritoryService,
    QueenslandService,
    SouthAustraliaService,
    TasmaniaService,
    VictoriaService,
    WesternAustraliaService,
    ServiceForm,
)
from .forms.add_service import AddQueenslandServiceForm

# Create your views here.
@login_required
def get_services(request):
    """
    Only used for testing purposes
    If a new service is created it will need to be added through an online interface
    by users with escalated privileges
    """
    from requests import get
    from itertools import chain
    from django.http import HttpResponse
    from django.utils.text import slugify
    from .models import State

    # Gets data from the "Do it online services" data set, using the CKAN data API
    # Example Record from API:
    # {
    #   '_id': 1,
    #   'interactionId': 'P000028',
    #   'service': 'Report fire ants',
    #   'service-url': 'https://www.business.qld.gov.au/industries/farms-fishing-forestry/agriculture/land-management/health-pests-weeds-diseases/pests/fire-ants-qld/reporting',
    #   'formerly': '',
    #   'details': '',
    #   'type': 'Report it',
    #   'type-slug': 'report-it',
    #   'category': 'Business and industry',
    #   'category-slug': 'business-and-industry',
    #   'available': 'yes',
    #   'kiosk-friendly': 'yes',
    #   'kiosk-only': 'no',
    #   'print-required': 'no',
    #   'osssio': 'no',
    #   'relevance': '',
    #   'qg-services': 'yes'
    #  }
    if not request.user.is_staff:
        raise PermissionDenied

    else:
        BASE_URL = "https://www.data.qld.gov.au"
        data = [
            get(
                BASE_URL + "/api/3/action/datastore_search?resource_id=384429ae-fd27-4448-afe6-e4ecb8d1ad93"
            ).json()
        ]

        # The API provides the total number of results in the resource
        # The offset is in increments of 100
        # Even if offset > total, the API will still return results
        # In an event where the total number of services changes, this loop will still work
        total, offset, i = data[0]["result"]["total"], 0, 0

        while offset < total:
            data.append(get(BASE_URL + data[i]["result"]["_links"]["next"]).json())
            i += 1
            offset = data[i]["result"]["offset"]

        results = list(chain(*[res["result"]["records"] for res in data]))

        no_entries = 0
        for service in results:
            if QueenslandService.objects.filter(interaction_id=service["interactionId"]).exists():
                no_entries += 1

            else:
                QueenslandService(
                    interaction_id=service["interactionId"],
                    name=service["service"],
                    name_slug=slugify(service["service"]),
                    url=service["service-url"],
                    description=service["details"],
                    state=State.QUEENSLAND,
                    type=service["type"],
                    type_slug=service["type-slug"],
                    category=service["category"],
                    category_slug=service["category-slug"],
                    available=True if service["available"] == "yes" else False,
                    kiosk_friendly=True if service["kiosk-friendly"] == "yes" else False,
                    kiosk_only=True if service["kiosk-only"] == "yes" else False,
                    print_required=True if service["print-required"] == "yes" else False,
                    osssio=True if service["osssio"] == "yes" else False,
                    relevance=service["relevance"],
                ).save()

        print(no_entries)
        if no_entries == total:
            return HttpResponse("<h1>200</h1><p>Queensland Services Up to Date</p>")

        return HttpResponse("<h1>200</h1><p>Queensland Services Updated</p>")


def service_redirect(request, state, service_name):
    if state == "act":
        url = AustralianCapitalTerritoryService().objects.get(name_slug=service_name).url

    elif state == "nsw":
        url = NewSouthWalesService().objects.get(name_slug=service_name).url

    elif state == "nt":
        url = NorthernTerritoryService().objects.get(name_slug=service_name).url

    elif state == "qld":
        url = QueenslandService().objects.get(name_slug=service_name).url

    elif state == "sa":
        url = SouthAustraliaService().objects.get(name_slug=service_name).url

    elif state == "tas":
        url = TasmaniaService().objects.get(name_slug=service_name).url

    elif state == "vic":
        url = VictoriaService().objects.get(name_slug=service_name).url

    elif state == "wa":
        url = WesternAustraliaService().objects.get(name_slug=service_name).url

    else:
        raise ViewDoesNotExist("The state you have requested does not exist")

    return redirect(url)


class ServiceFormView(FormView):
    model = ServiceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        # form.instance.service = Service.objects.get(name_slug=self.kwargs["service-name"])
        return super().form_valid(form)


class AddServiceView(FormView):
    """
    A view for adding a service to the database
    """

    template_name = "services/queensland/add_service.html"
    form_class = AddQueenslandServiceForm
    success_url = "/success/form"

    def form_valid(self, form):
        """
        If the form is valid, save the form and redirect to the success URL
        """
        form.save()
        return super().form_valid(form)
