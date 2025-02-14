from django.urls import path
from .views import generate_qrcodes

urlpatterns = [
    path('generate/', generate_qrcodes, name='generate_qrcodes'),
]