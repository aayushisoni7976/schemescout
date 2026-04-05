from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('check-profile/', views.login_redirect_view, name='check_profile'),
    path('whatsapp/', views.whatsapp_webhook, name='whatsapp_webhook'),
]