from django.urls import path
from .views import register_tree, login_view, contact

urlpatterns = [
    path('register/<uuid:qr_id>/', register_tree, name='register-tree'),
    path('login/', login_view, name='login-view'),
    path('contact/', contact, name='contact'),

]
