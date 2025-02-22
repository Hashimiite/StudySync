from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'), 
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('logout/', views.logout_view, name='logout_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('join-or-create/', views.join_or_create_group, name='join_or_create_group'),
    path('profile/', views.view_profile, name='view_profile'),
    path('group-chat/<int:group_id>/', views.group_chat, name='group_chat'),
    path('search/', views.search_groups, name='search_groups'),
]