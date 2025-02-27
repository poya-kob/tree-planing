from django.urls import path
from .views import user_dashboard, tree_list, tree_detail

urlpatterns = [
    path('dashboard/', user_dashboard, name='dashboard'),
    path('dashboard/trees', tree_list, name='trees-list'),
    path('dashboard/tree/<uuid:qr_id>', tree_detail, name='tree-detail'),

]
