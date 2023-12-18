from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('servers/', views.server_list, name='server_list'),
    path('logs/', views.connection_logs, name='connection_logs'),
    path('add-server/', views.add_vpn_server, name='add_vpn_server'),
    path('add-log/', views.add_connection_log, name='add_connection_log'),
    path('edit-server/<int:pk>/', views.edit_vpn_server, name='edit_vpn_server'),
    path('edit-log/<int:pk>/', views.edit_connection_log, name='edit_connection_log'),
    path('proxy/', views.show_proxy_page, name='show_proxy_page'),
    path('proxy-view/', views.proxy_view, name='proxy_view'),
    path('statistics/', views.statistics_view, name='statistics'),
]