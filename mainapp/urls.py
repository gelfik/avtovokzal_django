"""MIPS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index, name='main_url'),

    path('add_new_flight/', views.flight_edit_views, name='add_new_flight_url'),
    re_path(r'flight/([0-9]+)/', views.flight_views, name='flight_url'),

    re_path(r'bus/([0-9]+)/(delete)', views.bus_edit_views, name='bus_edit_url'),
    path('bus/', views.bus_views, name='bus_list_url'),

    re_path(r'ticket/([0-9]+)/', views.ticket_views, name='ticket_url'),
    re_path(r'sell/([0-9]+)/', views.sell_views, name='sell_url'),

    re_path(r'users/([0-9]+)/(delete|edit)', views.user_edit_views, name='user_edit_url'),
    path('users/', views.user_list_views, name='user_list_url'),

    path('user/', include('userapp.urls')),

    # re_path(r'order/([0-9]+)/(pay|cancel|accept|info)/', views.order_edit_views, name='order_edit_url'),
    # re_path(r'order/([0-9]+)/', views.order_views, name='order_url'),
    # path('order/', views.order_list_views, name='order_list_url'),
    #
    # re_path(r'order_arhive/([0-9]+)/', views.order_arhive_views, name='order_arhive_url'),
    # path('order_arhive/', views.order_arhive_list_views, name='order_arhive_list_url'),
    #
    # path('car/', views.car_views, name='car_add_url'),
]
