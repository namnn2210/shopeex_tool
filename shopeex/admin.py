from django.contrib import admin
from .models import ProcessData
# Register your models here.
class CustomProcessData(admin.ModelAdmin):
    list_display = ('user', 'cookie', 'username', 'password','status','created_at',)
    list_filter = ('user', 'status','created_at',)
    search_fields = ('user', 'cookie', 'username', 'status','created_at',)
    ordering = ('created_at',)

admin.site.register(ProcessData, CustomProcessData)
