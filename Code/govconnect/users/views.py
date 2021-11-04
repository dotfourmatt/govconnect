from django.shortcuts import render
from .forms import GovConnectAuthenticationForm
from .auth import GovConnectUserAuthenticationBackend


def login_page(request):
    form = GovConnectAuthenticationForm()
    context = {"form": form}

    if request.method == "POST":
        form = GovConnectAuthenticationForm(request.POST)

    return render(request, "users/login.html", context)
