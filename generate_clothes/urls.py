from django.urls import path
from .views import *
from .import views

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('settings', Settings.as_view(), name='settings'),
    path('style/<str:slug>/', show_style, name='show_style')
]
