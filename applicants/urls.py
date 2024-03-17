
from django.contrib import admin
from django.urls import path, include
from applicants import views

urlpatterns = [
    path("register/", views.PublicUserRegistrationView.as_view(), name='register'),
    path("login/", views.PublicUserLoginView.as_view(), name='login'),
    path("profile/", views.PrivateApplicantProfile.as_view(), name='profile'),
]
