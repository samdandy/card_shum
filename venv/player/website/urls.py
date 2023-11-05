"""
URL configuration for player project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('card_lookup/', views.card_lookup_page, name='card_lookup'),
    path('record/<int:pk>',views.customer_record,name='record'),
    path('delete_card/<int:pk>',views.delete_card,name='delete_card'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>',views.update_record,name='update_record'),
    path('image_upload/',views.image_uploader,name='image_upload'),
]
