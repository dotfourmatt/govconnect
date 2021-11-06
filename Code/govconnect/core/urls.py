from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from users.views import login_page, two_step_verification

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_page, name="user-login"),
    path("account/", include("users.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
