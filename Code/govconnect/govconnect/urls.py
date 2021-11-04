from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="users-login",
    ),
    path("u/", include("users.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
