from django.urls import path
from .views import register_tree, login_view, contact, register

urlpatterns = [
    path('register/<uuid:qr_id>/', register_tree, name='register-tree'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login-view'),
    path('contact/', contact, name='contact'),

]
