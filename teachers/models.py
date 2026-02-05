from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institute_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    joined_on = models.DateField(auto_now_add=True)
    subscription_expiry = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.institute_name
    
    def check_subscription(self):

        if self.subscription_expiry:
            if self.subscription_expiry < timezone.now().date():
                self.is_active = False
                self.save()