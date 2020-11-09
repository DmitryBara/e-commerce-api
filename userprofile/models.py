from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Subscribe(models.Model):
    start = models.DateField(auto_now_add=True)
    finish = models.DateField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, default='aaaaa')
    subscribe = models.ForeignKey(Subscribe, null=True, blank=True, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw'):
        Profile.objects.create(user=instance, token=instance.token)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Subscribe)
def update_subscribe_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.get(pk=instance.related_profile)
        profile.subscribe = instance
        profile.save()
