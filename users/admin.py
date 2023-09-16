from django.contrib import admin

# Register your models here.
from .models import CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined',)
    list_filter = ('is_active', 'date_joined',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    ordering = ('-date_joined',)

admin.site.register(CustomUser, CustomUserAdmin)