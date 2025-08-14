from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from app.accounts.models import UserProfile
from app.subscribtions.models import Subscription

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
                
        free_plan = Subscription.objects.filter(
            package_type=Subscription.PackageType.FREE,
            status=True
        ).first()
        if free_plan:
            profile.subscription_plan = free_plan
            profile.save()
        else:
            free_plan = Subscription.objects.create(
                package_amount=0,
                package_type=Subscription.PackageType.FREE,
                status=True
            )
            profile.subscription_plan = free_plan
            profile.save()