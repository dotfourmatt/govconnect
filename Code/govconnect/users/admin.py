from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import GovConnectUser, Service


class UserAdmin(BaseUserAdmin):
    model = GovConnectUser
    list_display = (
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "address",
        "date_of_birth",
        "primary_identification",
        "primary_identification_number",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_staff", "primary_identification")

    search_fields = (
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "primary_identification_number",
    )
    ordering = ("-date_created",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "date_of_birth",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        (
            "Personal",
            {
                "fields": (
                    "primary_identification",
                    "primary_identification_number",
                    "address",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "address",
                    "date_of_birth",
                    "primary_identification",
                    "primary_identification_number",
                    "is_active",
                    "is_staff",
                )
            },
        ),
    )


# Register your models here.
admin.site.register(GovConnectUser, UserAdmin)
# admin.site.register(Service)

admin.site.unregister(Group)
