from django.contrib import admin
from . import models

@admin.register(models.History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'query', 'date']
    list_display_links = ['id', 'query', 'date']
    list_filter = ['date'] 
