from django.contrib import admin
from . models import Teacher
# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        'institute_name',
        'phone',
        'is_active',
        'subscription_expiry'
    )
    list_filter = ('is_active',)
    search_fields = ('institute_name', 'phone')
    
    def has_add_permission(self, request):
        return False