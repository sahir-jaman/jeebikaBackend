from django.urls import path
from employees import views

urlpatterns = [
    path("register/", views.PublicEmployeeRegistrationView.as_view(), name='register'),
    path("login/", views.PublicEmployeeLogin.as_view(), name='login'),
    path("profile/", views.PrivateEmployeeProfile.as_view(), name='profile'),
    path("posts/", views.PrivateEmployeeposts.as_view(), name='posts'),
    path("posts/<uuid:post_uid>/", views.PrivateEmployeePostDetail.as_view(), name='post_detail'),
]
