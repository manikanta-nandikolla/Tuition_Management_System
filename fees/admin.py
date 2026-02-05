from django.contrib import admin
from .models import Fee
# Register your models here.
@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'month',
        'year',
        'amount',
        'payment_mode',
        'paid_on',
        'receipt_no'
    )

    list_filter = ('month', 'year', 'payment_mode')
    search_fields = ('student__name', 'receipt_no')