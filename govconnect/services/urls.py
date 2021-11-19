from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import get_services, AddServiceView, service_redirect, ServiceFormView
from users.views import search_services

urlpatterns = [
    path("api/update/", get_services, name="api-update"),
    path("api/search/", csrf_exempt(search_services), name="api-search"),
    path("<str:state>/<str:service_name>/", service_redirect, name="service-redirect"),
    path("<str:state>/<str:service_name>/form/", ServiceFormView.as_view(), name="service-form"),
]
