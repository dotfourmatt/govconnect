from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        auth_views.LoginView.as_view(template_name="users/landing.html"),
        name="users-login",
    ),
    path("u/", include("users.urls")),
]
