from django.urls import path

from .views import get_services, AddServiceView, service_redirect


urlpatterns = [
    path("<str:state>/<str:service-name>/", service_redirect, name="service-redirect"),
    path("<str:state>/<str:service-name>/form/")
]
