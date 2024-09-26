from rest_framework.urls import path
from .views import hello_user_with_name, hello_world


urlpatterns = [
    path('', hello_world),
    path('hello/<str:name>/', hello_user_with_name),
]