
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.db import IntegrityError

# Create signals

### Signals to create new user profile attached to default users by django auth

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Signal to check if there is already a superuser
@receiver(post_save, sender=User)
def make_first_user_superuser(sender, instance, created, **kwargs):
    if created:  # Only run if a new user is created
        print(f"New user created: {instance.username}")

        # Check if there's already a superuser
        if not User.objects.filter(is_superuser=True).exists():
            try:
                print(f"Making {instance.username} a superuser as the first user.")
                # Make the first user a superuser
                instance.is_superuser = True
                instance.is_staff = True  # Optional: If you want them to be staff as well
                instance.save()
            except IntegrityError as e:
                print(f"Error while creating superuser: {e}")