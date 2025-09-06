# Auto-create accounts when a user registers
# ----------------------------------------------------

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Account


@receiver(post_save, sender=User)
def create_user_profile_and_accounts(sender, instance, created, **kwargs):
    if created:
        # Create Profile
        # ----------------------------------------------------
        Profile.objects.create(user = instance, first_name = instance.first_name, last_name = instance.last_name)

        # Create Checking and Savings Accounts
        # ----------------------------------------------------
        Account.objects.create(user = instance, kind = Account.CHECKING)
        Account.objects.create(user = instance, kind = Account.SAVINGS)