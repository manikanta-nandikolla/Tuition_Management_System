from django.db import models
from teachers.models import Teacher
# Create your models here.
class Student(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="students", null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name