from rest_framework.urls import path

# from .views import get_items, create_item, delete_user
from .views import get_items, delete_item

urlpatterns = [
    path('', get_items, name='Get All Items'),
    # path('newitem/', create_item, name='Create Item'),
    path('remove/item', delete_item, name='Delete Item'),
    # path('get_current_user/', get_current_user, name='Get Current User'),
]

