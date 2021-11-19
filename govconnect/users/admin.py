from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import GovConnectUser, EnabledServices


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
        "address" "primary_identification_number",
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
        ("Permissions", {"fields": ("is_staff", "is_superuser")}),
        (
            "Personal",
            {
                "fields": (
                    "primary_identification",
                    "primary_identification_number",
                    "address",
                    "street_address",
                    "suburb",
                    "state",
                    "postcode",
                )
            },
        ),
        (
            "Security",
            {
                "fields": (
                    "secret_question",
                    "secret_question_answer",
                    "sms_one_time_password",
                    "email_one_time_password",
                    "passwordless_login",
                    "physical_security_authentication",
                )
            },
        ),
        ("Other", {"fields": ("date_created", "is_active", "last_login", "last_login_ip")}),
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
                    "street_address",
                    "suburb",
                    "state",
                    "postcode",
                    "secret_question",
                    "secret_question_answer",
                    "primary_identification",
                    "primary_identification_number",
                    "is_active",
                    "is_staff",
                )
            },
        ),
    )

    readonly_fields = (
        "address",
        # "secret_question",
        # "secret_question_answer",
        "sms_one_time_password",
        "email_one_time_password",
        "passwordless_login",
        "physical_security_authentication",
        "date_created",
        "last_login",
        "last_login_ip",
    )

    # Only superusers can change details
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        return False


# Register your models here.
admin.site.register(GovConnectUser, UserAdmin)
admin.site.register(EnabledServices)
# admin.site.register(Service)

admin.site.unregister(Group)
