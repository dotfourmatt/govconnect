from django.urls import path

from .views import get_services, AddServiceView, service_redirect, ServiceFormView


urlpatterns = [
    path("<str:state>/<str:service_name>/", service_redirect, name="service-redirect"),
    path("<str:state>/<str:service_name>/form/", ServiceFormView.as_view(), name="service-form"),
]
