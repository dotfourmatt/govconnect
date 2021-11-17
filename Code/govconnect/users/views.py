from json import loads

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import MultipleObjectMixin
from django.utils.text import slugify

from .backends import GovConnectUserAuthenticationBackend
from .forms import GovConnect2FactorAuthenticationForm, GovConnectAuthenticationForm, UpdateGovConnectUserForm
from .models import EnabledServices, GovConnectUser
from services.models import QueenslandService


#! Convert to Class Based View
def login_page(request):
    form = GovConnectAuthenticationForm()
    context = {"form": form}

    if request.method == "POST":
        form = GovConnectAuthenticationForm(request.POST)

        user = GovConnectUserAuthenticationBackend().authenticate(
            request,
            id_type=request.POST["id_type"],
            id_num=request.POST["username"],
            date_of_birth=request.POST["date_of_birth"],
        )

        if user is not None:
            request.session["pk"] = user.pk
            return redirect("user-auth")

    return render(request, "users/login.html", context)


#! Convert to Class Based View
def two_step_verification(request):
    form = GovConnect2FactorAuthenticationForm(request.POST)
    pk = request.session.get("pk")

    if pk:
        # Will add ways for other methods of authentication
        # Flags for other MFA types will be used to check this.
        user = GovConnectUser.objects.get(pk=pk)
        answer_hash = user.secret_question_answer

        if not request.POST:
            # If using other 2-factor authentication methods,
            # this would be where the code would be, but it hasn't been created yet
            pass

        if form.is_valid():
            answer = form.cleaned_data.get("secret_question_answer")
            if check_password(answer, answer_hash):
                login(request, user)
                return redirect("user-home")
            else:
                return redirect("user-login")
    else:
        return redirect("user-login")

    return render(
        request,
        "users/two_step_verification.html",
        context={"form": form, "question": user.secret_question},
    )


# class UserHomeView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
# class UserHomeView(LoginRequiredMixin, UserPassesTestMixin, MultipleObjectMixin, ListView):
# ? Needs to be Detail View and List View
# ? For User details and the search box respectively
class UserHomeView(LoginRequiredMixin, DetailView):
    template = "users/user_home.html"
    model = GovConnectUser

    def get(self, request):
        return render(request, "users/account.html")


class UserSettingsView(LoginRequiredMixin, UpdateView):
    model = GovConnectUser
    form_class = UpdateGovConnectUserForm
    template = "users/settings.html"

    def get(self, request, *args, **kwargs):
        services = EnabledServices.objects.get(user=request.user).services
        federal = {key: value for key, value in sorted(services["Federal"].items())}
        state = {key: value for key, value in sorted(services["State"].items())}
        form = self.form_class(instance=request.user)

        return render(
            request,
            self.template,
            context={"form": form, "federal_services": federal, "state_services": state},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        services = EnabledServices.objects.get(user=request.user).services
        federal = {key: value for key, value in sorted(services["Federal"].items())}
        state = {key: value for key, value in sorted(services["State"].items())}

        if form.is_valid():
            form.save()
            messages.success(request, "Your details have been updated successfully!")
            return redirect("user-settings")

        messages.error(request, "There was an error updating your details.")
        return render(
            request, self.template, context={"form": form, "federal_services": federal, "state_services": state}
        )


def update_enabled_services(request, *args, **kwargs):
    es = EnabledServices.objects.get(user=request.user)
    services_enabled_by_user = es.services
    enabled = {name: True if value == "on" else False for name, value in request.POST.items()}
    del enabled["csrfmiddlewaretoken"]

    for service_region in services_enabled_by_user:
        for service, value in services_enabled_by_user[service_region].items():
            # Checks if the service is currently enabled by the user, but is not in the request
            # Therefore, the user has opted out of the service
            if service not in enabled and value:
                services_enabled_by_user[service_region][service] = False

            # Checks if the service is currently disabled by the user, but is in the request
            elif service in enabled and value != enabled[service]:
                services_enabled_by_user[service_region][service] = enabled[service]

    es.services = services_enabled_by_user
    es.save()
    return redirect("user-settings")


# API Endpoint for service searching
def search_services(request):
    if request.method == "POST":
        search_term = loads(request.body).get("search_term")
        if search_term:
            enabled_services = EnabledServices.objects.get(user=request.user).services
            federal_enabled = [slugify(s) for s, v in enabled_services["Federal"].items() if v]
            state_enabled = [slugify(s) for s, v in enabled_services["State"].items() if v]

            if request.user.state == "ACT":
                pass

            elif request.user.state == "NSW":
                pass

            elif request.user.state == "NT":
                pass

            elif request.user.state == "SA":
                pass

            elif request.user.state == "TAS":
                pass

            elif request.user.state == "VIC":
                pass

            elif request.user.state == "QLD":
                results = QueenslandService.objects.filter(name__icontains=search_term)

            elif request.user.state == "WA":
                pass

            results = (
                results.filter(category_slug__in=federal_enabled)
                | results.filter(category_slug__in=state_enabled)
            ).distinct()
            data = list(results.values())

            return JsonResponse(data, safe=False)
