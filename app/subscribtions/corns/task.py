from django.utils import timezone
from django_cron import CronJobBase, Schedule
from app.subscribtions.models import Subscription
from app.accounts.models import UserProfile

class DowngradeExpiredSubscriptionsCron(CronJobBase):
    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'myapp.downgrade_expired_plans'

    def do(self):
        free_plan = Subscription.objects.filter(
            package_type=Subscription.PackageType.FREE
        ).first()
        now = timezone.now()
        expired_profiles = UserProfile.objects.filter(
            subscription_end__lt=now
        )
        for profile in expired_profiles:
            profile.subscription_plan = free_plan
            profile.subscription_start = None
            profile.subscription_end = None
            profile.save()
