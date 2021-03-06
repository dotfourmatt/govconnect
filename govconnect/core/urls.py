from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from users.views import login_page
from .views import RegisterHelpView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_page, name="user-login"),
    path("help/register/", RegisterHelpView.as_view(), name="register-help"),
    path("account/", include("users.urls")),
    path("service/", include("services.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
