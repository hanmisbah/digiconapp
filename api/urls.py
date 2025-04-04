from django.urls import path
from .views import RegisterView, LoginView, AdminOnlyView, UserOnlyView, UserProfileView, ChangePasswordView, LogoutView,ListUsersView,DeleteUserView
from rest_framework import status
from .views import ImageUploadView
from.views import  CreateContainerView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin-dashboard/', AdminOnlyView.as_view(), name='admin-dashboard'),
    path('user-dashboard/', UserOnlyView.as_view(), name='user-dashboard'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
    path('user-only/', UserOnlyView.as_view(), name='user-only'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', ListUsersView.as_view(), name='list-users'),
    path('delete-account/', DeleteUserView.as_view(), name='delete-account'),
    path('upload-image/', ImageUploadView.as_view(), name='upload-image'),
     path('create-container/', CreateContainerView.as_view(), name='create-container'),



]
