from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import GovConnectUser, EnabledServices
from services.models import QueenslandService


@receiver(post_save, sender=GovConnectUser)
def create_enabled_services(sender, instance, created, **kwargs):
    if created:
        es = EnabledServices.objects.create(user=instance)
        if es.user.state == "ACT":
            pass
        elif es.user.state == "NSW":
            pass
        elif es.user.state == "NT":
            pass
        elif es.user.state == "QLD":
            es.services = {
                "Federal": {"Centrelink": False, "Medicare": False, "Child Support": False},
                "State": {
                    category: False
                    for category in QueenslandService.objects.order_by("category")
                    .values_list("category", flat=True)
                    .distinct()
                },
            }
        elif es.user.state == "SA":
            pass
        elif es.user.state == "TAS":
            pass
        elif es.user.state == "VIC":
            pass
        elif es.user.state == "WA":
            pass


@receiver(post_save, sender=GovConnectUser)
def update_enabled_services(sender, instance, **kwargs):
    instance.enabled_services.save()
