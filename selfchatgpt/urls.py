from django.urls import path, include
from . import views

app_name = 'selfchatgpt'
urlpatterns = [
    path('', views.index, name='index'),
    path('chat', views.chat, name='chat'),
]