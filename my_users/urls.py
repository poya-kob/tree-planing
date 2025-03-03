from django.urls import path
from .views import register_tree, login_view, contact, logout_page

urlpatterns = [
    path('register/<uuid:qr_id>/', register_tree, name='register-tree'),
    # path('register/', register, name='register'),
    path('login/', login_view, name='login-view'),
    path('logout/', logout_page, name='log-out'),
    path('contact/', contact, name='contact'),

]
