from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.scan_document, name='scan_document'),
    path('cancel-scan/', views.cancel_scan, name='cancel_scan'),
    path('reset-form/', views.reset_form, name='reset_form'),
    path('', views.home, name='home'),
]
