from django.urls import path
from .views import *
from .import views

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('<str:season>/style/', StylesPage.as_view(), name='styles_page'),
    path('<str:season>/style/<str:slug>/', Style.as_view(), name='show_style'),
    path('settings/', Settings.as_view(), name='settings'),
]