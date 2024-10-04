from rest_framework.urls import path

from .views import get_users, create_user, login, get_current_user, logout, delete_user

urlpatterns = [
    path('newuser/', create_user, name='Create User'),
    path('login/', login, name='Login'),
    path('logout/', logout, name='Logout'),
    path('delete/user', delete_user, name='Delete User'),
    path('users/', get_users, name='Get All Users'),
    path('get_current_user/', get_current_user, name='Get Current User'),
]