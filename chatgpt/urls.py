# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views

app_name = 'chatgpt'
urlpatterns = [
    path('', views.chat, name='chat'),    
]
