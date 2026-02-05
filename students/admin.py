from django.contrib import admin
from .models import Student
# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'phone',
        'gender',
        'joined_date',
        'is_active'
    )

    list_filter = ('gender', 'is_active')

    search_fields = ('name', 'phone')