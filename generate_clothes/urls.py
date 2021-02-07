from django.urls import path
from .views import *
from .import views

urlpatterns = [
    path('', Settings.as_view(), name='settings'),
    path('season/', Seasons.as_view(), name='seasons'),
    path('season/<str:season>/style/', StylesPage.as_view(), name='styles_page'),
    path('season/<str:season>/style/<str:slug>/', Style.as_view(), name='show_style'),
]