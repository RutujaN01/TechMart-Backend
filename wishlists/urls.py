from rest_framework.urls import path

from .views import create_wishlist, get_all_wishlists_for_current_user, get_wishlist_by_id, update_wishlist, \
    delete_wishlist, \
    get_all_items_for_current_user, add_item_to_wishlist

urlpatterns = [
    path('', get_all_wishlists_for_current_user, name='Get All Wishlists'),
    path('items', get_all_items_for_current_user, name='Get All Items For Current User'),
    path('new', create_wishlist, name='Create Wishlist'),
    path('get/<str:wishlist_id>/', get_wishlist_by_id, name='Get Wishlist By ID'),
    path('add-item', add_item_to_wishlist, name='Add Item To Wishlist'),
    path('update', update_wishlist, name='Update Wishlist'),
    path('delete', delete_wishlist, name='Delete Wishlist'),
]
