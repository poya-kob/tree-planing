from django.urls import path
from .views import user_dashboard, TreeDetailView, UnapprovedImagesView, ApproveImagesView, TreeListView, \
    CommentsListView
from blog.views import create_blog

urlpatterns = [
    path('', user_dashboard, name='dashboard'),
    path('trees', TreeListView.as_view(), name='trees-list'),
    path('tree/<slug:unique_id>/', TreeDetailView.as_view(), name="tree-detail"),
    path('images/unapproved/', UnapprovedImagesView.as_view(), name='unapproved-images'),
    path('images/approve/', ApproveImagesView.as_view(), name='approve-images'),
    path('create-post/', create_blog, name='create-post'),
    path('comments/', CommentsListView.as_view(), name='comments-list'),

]
