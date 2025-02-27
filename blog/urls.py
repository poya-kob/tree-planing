from django.urls import path

from .views import blog_list, blog_detail

urlpatterns = [
    path('blogs/', blog_list, name='blogs'),
    path('blogs/<blog_id>/', blog_detail, name='blogs-detail'),

]
