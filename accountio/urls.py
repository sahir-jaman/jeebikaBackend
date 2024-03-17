from django.contrib import admin
from django.urls import path, include
from accountio import views

urlpatterns = [
    path("register/", views.PublicUserRegistration.as_view(), name='register'),
]
