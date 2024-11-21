from django.contrib import admin
from django.urls import path
from self_service import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.custom_login, name='login'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Logout path pointing to the logout_view

    # Admin paths
    path('upload/', views.upload_excel, name='upload_excel'),
    path('admin-notifications/', views.admin_notifications, name='admin-notifications'),
    path('admin-new-query/', views.admin_new_query),
    path('admin-reply/', views.admin_new_query, name='admin_new_query'),

    path('admin-queries/', views.admin_old_query, name='admin_old_query'),
    path('admin-about/', views.admin_about),
    path('admin-feedback/', views.admin_feedback, name='admin_feedback'),

    # User paths
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user-notifications/', views.user_notifications),
    path('user-pf-status/', views.user_pf_status),
    path('submit-query/', views.user_new_query, name='user_new_query'),
    path('my-queries/', views.user_my_query, name='user_my_query'),
    path('user-about/', views.user_about),
    path('user-feedback/', views.user_feedback, name='user_feedback'),
]