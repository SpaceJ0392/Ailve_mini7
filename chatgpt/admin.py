from django.contrib import admin
from django.urls import path
from . import models

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Register your models here.
@admin.register(models.History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'query', 'date']
    list_display_links = ['id', 'query', 'date']
    list_filter = ['date'] 

