from django.db import models
from students.models import Student
from teachers.models import Teacher
import uuid
# Create your models here.
class Fee(models.Model):

    PAYMENT_MODE = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('bank', 'Bank Transfer'),
    ]

    MONTH_CHOICES = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="fees", null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fees")
    month = models.CharField(max_length=2, choices=MONTH_CHOICES)
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE)
    paid_on = models.DateField(auto_now_add=True)
    receipt_no = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.month}"