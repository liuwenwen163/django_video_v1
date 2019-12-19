# encoding: utf-8
from django.urls import path, include
from app.dashboard.views.auth import Login, AdminManager, Logout, UpdateAdminStatus
from .views.base import Index

__author__ = 'bbw'


urlpatterns = [
    path('', Index.as_view(), name='dashboard_index'),
    path('login', Login.as_view(), name='dashboard_login'),
    path('logout', Logout.as_view(), name='logout'),
    path('admin/manager', AdminManager.as_view(), name='admin_manager'),
    path('admin/manager/update/status', UpdateAdminStatus.as_view(), name='admin_update_status')
]
