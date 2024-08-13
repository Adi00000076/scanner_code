from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.scan_document, name='scan'),
    path('cancel-scan/', views.cancel_scan, name='cancel_scan'),
    path('reset-form/', views.reset_form, name='reset_form'),
    # Add other URL patterns as needed
]