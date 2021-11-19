from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.UserHomeView.as_view(), name="user-home"),
    path("auth/", views.two_step_verification, name="user-auth"),
    path(
        "logout/",
        LogoutView.as_view(template_name="users/logout.html", next_page="/"),
        name="user-logout",
    ),
    path("settings/", views.UserSettingsView.as_view(), name="user-settings"),
    path("settings/update/services", views.update_enabled_services, name="user-update-enabled-services"),
]
