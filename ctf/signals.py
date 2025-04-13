from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserAnswer, UserProfile

@receiver(post_save, sender=UserAnswer)
def update_user_profile(sender, instance, created, **kwargs):
    user_profile, created = UserProfile.objects.get_or_create(user=instance.user)

    if instance.is_correct:
        user_profile.points += 1  # Increment points by 1 for a correct answer
        user_profile.challenges_solved += 1  # Increment challenges solved
        user_profile.save()