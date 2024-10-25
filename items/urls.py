from rest_framework.urls import path

# from .views import get_items, create_item, delete_user
from .views import get_items, delete_item, create_item, update_item, getItem, getItemByName, getItemsByCat

urlpatterns = [
    path('', get_items, name='Get All Items'),
    path('newitem', create_item, name='Create Item'),
    path('remove/item', delete_item, name='Delete Item'),
    path('update/item', update_item, name='Update Item'),
    path('getItem/item', getItem, name = 'Get specifit Item'),
    path('searchName/<str:item_name>', getItemByName, name = 'Get Item by name'),
    path('searchCat/item', getItemsByCat, name = 'Get Items by cat'),

]

