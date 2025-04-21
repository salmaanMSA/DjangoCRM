from django.contrib.auth.models import User
from .models import Customer
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def createCustomerProfile(sender, instance, created, **kwargs):
    print(sender, instance, created, kwargs)
    if created:
        Customer.objects.create(
            user = instance,
            name = instance.username,
            email = instance.email
        )
        print("customer profile created")