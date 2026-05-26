from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'membership_type', 'phone']
    list_filter = ['role', 'membership_type']
    search_fields = ['user__username', 'phone']
