from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# from django.contrib.auth.views import LoginView
from .forms import GovConnectAuthenticationForm, GovConnect2FactorAuthenticationForm
from .auth import GovConnectUserAuthenticationBackend
from .models import GovConnectUser

# class AuthView(LoginView):
#    template_name = 'govconnect/login.html'
#    authentication_form = GovConnectAuthenticationForm


def login_page(request):
    form = GovConnectAuthenticationForm()
    context = {"form": form}

    if request.method == "POST":
        form = GovConnectAuthenticationForm(request.POST)

        user = GovConnectUserAuthenticationBackend().authenticate(
            request,
            id_type=request.POST["id_type"],
            id_num=request.POST["id_num"],
            date_of_birth=request.POST["date_of_birth"],
        )

        if user is not None:
            request.session["pk"] = user.pk
            return redirect("user-auth")

    return render(request, "users/login.html", context)


def two_step_verification(request):
    form = GovConnect2FactorAuthenticationForm(request.POST or NONE)
    pk = request.session.get("pk")

    if pk:
        user = GovConnect.objects.get(pk=pk)
        answer_hash = user.secret_question_answer

        if not request.POST:
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


class UserHomeView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template = "users/user_home.html"
    model = GovConnectUser

    def get(self, request):
        return render(request, "users/user_home.html")

    def text_func(self):
        return False
