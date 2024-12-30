from django.contrib import admin

from django.contrib import admin
from .models import Profile,Registration

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'last_name')
    search_fields = ('firstname', 'last_name', 'user__username')
    list_filter = ('user__is_active',)

admin.site.register(Profile, ProfileAdmin)




@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'program_title', 'email']
    list_filter = ['program_title', 'education_level']
    search_fields = ['first_name', 'last_name', 'email']
