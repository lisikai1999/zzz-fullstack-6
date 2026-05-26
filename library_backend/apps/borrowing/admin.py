from django.contrib import admin
from .models import BorrowingRecord, BorrowingConfig

@admin.register(BorrowingConfig)
class BorrowingConfigAdmin(admin.ModelAdmin):
    list_display = ['membership_type', 'max_borrow_days', 'max_renew_times', 'fine_per_day']

@admin.register(BorrowingRecord)
class BorrowingRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrow_date', 'due_date', 'status']
    list_filter = ['status']
    search_fields = ['user__username', 'book__title']
