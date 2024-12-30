from django.contrib import admin

from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'last_name')
    search_fields = ('firstname', 'last_name', 'user__username')
    list_filter = ('user__is_active',)

admin.site.register(Profile, ProfileAdmin)
