from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_related_models(sender, instance, created, **kwargs):
    if created:
        # Only create if it doesn't exist
        Profile.objects.get_or_create(user=instance)