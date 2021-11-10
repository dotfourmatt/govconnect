from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView

from .backends import GovConnectUserAuthenticationBackend
from .forms import GovConnect2FactorAuthenticationForm, GovConnectAuthenticationForm
from .models import GovConnectUser

# from django.contrib.auth.views import LoginView
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
            id_num=request.POST["username"],
            date_of_birth=request.POST["date_of_birth"],
        )

        if user is not None:
            request.session["pk"] = user.pk
            return redirect("user-auth")

    return render(request, "users/login.html", context)


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
class UserHomeView(LoginRequiredMixin, DetailView):
    template = "users/user_home.html"
    model = GovConnectUser

    def get(self, request):
        return render(request, "users/account.html")

    # def test_func(self):
    #    return False
