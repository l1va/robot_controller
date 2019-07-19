from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='mobile_platform-home'),
    path('command/', views.command, name='mobile_platform-command')
]
