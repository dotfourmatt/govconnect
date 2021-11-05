from django.urls import path
from . import views

urlpatterns = [path("", views.UserHomeView.as_view(), name="user-home")]
