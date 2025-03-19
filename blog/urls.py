from django.urls import path

from .views import BlogListView, BlogDetailView

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blogs'),
    path('blogs/category/<int:category_id>/', BlogListView.as_view(), name='blog_list_by_category'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blogs-detail'),

]
