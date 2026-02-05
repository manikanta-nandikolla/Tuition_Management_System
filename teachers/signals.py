from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Teacher

@receiver(post_save, sender=User)
def create_teacher(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Teacher.objects.create(user=instance, institute_name=instance.username, phone="")