from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import SysUser

@receiver(post_save, sender=User)
def create_SysUser(sender, instance, created, **kwargs):
    if created:
        SysUser.objects.create(user=instance)