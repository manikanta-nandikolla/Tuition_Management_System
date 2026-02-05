from django import forms
from .models import Fee
from datetime import datetime
from students.models import Student

class FeeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["student"].queryset = Student.objects.filter(teacher=user.teacher)
            
    class Meta:

        model = Fee

        fields = [
            'student',
            'month',
            'year',
            'amount',
            'payment_mode',
            'remarks'
        ]

        widgets = {

            'student': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'month': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'amount': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'payment_mode': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'remarks': forms.Textarea(
                attrs={'class': 'form-control'}
            ),
        }