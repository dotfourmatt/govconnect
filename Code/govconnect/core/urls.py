from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users.views import login_page, two_step_verification

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_page, name="users-login"),
    path("auth/", two_step_verification, name="user-auth"),
    path("account/", include("users.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
