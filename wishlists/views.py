from django.contrib.auth.hashers import check_password
from mongoengine.errors import NotUniqueError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from decorators import admin_route
from items.models import Items
from items.serializers import ItemsSerializer
from users.models import User
from .models import Wishlists
from .serializers import WishlistsSerializer

@api_view(['GET'])
def test(request):
    user = User.objects(username="admin").first()

    Items.objects(name=r"item*").delete()
    items = []
    for i in range(5):
        item = Items(name=f"item{i}", price=10.0)
        items.append(item)

    [item.save() for item in items]
    Wishlists.objects().delete()
    wishlist = Wishlists(name="wishlist1", user=user.id, items=items)
    wishlist.save()
    print(wishlist.user)
    print(wishlist.items)

    return_wishlist = Wishlists.objects(name="wishlist1").first()
    wishlist_data = WishlistsSerializer(return_wishlist).data
    del wishlist_data["user"]["password"]
    return Response({"data": wishlist_data})

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_wishlist(request):
    # Extract the wishlist data from the request and create a new wishlist
    wishlist_data = request.data
    wishlist = Wishlists(**wishlist_data)

    # If the user is an admin, they can create a wishlist for another user
    if request.user.is_staff:
        # Handle the case where the admin is creating a wishlist for another user
        if "user" in wishlist_data and wishlist_data["user"] != str(request.user.id):
            user = User.objects(id=wishlist_data["user"]).first()
            if user is None:
                return Response({"error": "User does not exist"}, status=400)
            wishlist.user = user

        # Handle the case where the admin is creating a wishlist for themselves
        else:
            wishlist.user = request.user
    # Handle cases where the user is not an admin
    else:
        # If the user is not an admin, they can only create a wishlist for themselves
        if "user" in wishlist_data and wishlist_data["user"] != str(request.user.id):
            return Response({"error": "You do not have permission to create a wishlist for another user"}, status=403)
        wishlist.user = request.user

    # Save the wishlist to the database
    try:
        wishlist.save()
    except NotUniqueError as e:
        # If the wishlist already exists, return an error
        return Response({"error": "Wishlist already exists with that information"}, status=400)
    except Exception as e:
        # If there is an error saving the wishlist, return the
        return Response({"error": str(e)}, status=400)

    # Serialize the wishlist data and return it
    wishlist_data = WishlistsSerializer(wishlist).data
    return Response({"data": wishlist_data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_items_for_current_user(request):
    # Extract all items that are in the current user's wishlists
    wishlists = Wishlists.objects(user=request.user)
    items = []

    for wishlist in wishlists:
        items.extend(wishlist.items)

    # Serialize the item data and return it
    items_data = ItemsSerializer(items, many=True).data
    return Response({"data": items_data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_wishlists_for_current_user(request):
    # Extract all wishlists from the database
    wishlists = Wishlists.objects(user=request.user)

    # Serialize the wishlist data and return it
    wishlists_data = WishlistsSerializer(wishlists, many=True).data
    return Response({"data": wishlists_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist_by_id(request, wishlist_id):
    # Extract the wishlist from the database
    wishlist = Wishlists.objects(id=wishlist_id).first()

    # If the wishlist does not exist, return an error
    if wishlist is None:
        return Response({"error": "Wishlist does not exist"}, status=404)

    # If the user is not the owner of the wishlist and the wishlist is not public, return an error
    if not request.user.is_staff:
        if wishlist.user != request.user and not wishlist.isPublic:
            return Response({"error": "You do not have permission to view this wishlist"}, status=403)

    # Serialize the wishlist data and return it
    wishlist_data = WishlistsSerializer(wishlist).data
    return Response({"data": wishlist_data})


    # Update the wishlist data
    wishlist.update(**wishlist_data)

    # Serialize the wishlist data and return it
    wishlist_data = WishlistsSerializer(wishlist).data
    return Response({"data": wishlist_data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_wishlist(request, wishlist_id):
    # Find the wishlist by ID
    wishlist = Wishlists.objects(id=wishlist_id).first()

    # Delete the wishlist
    wishlist.delete()

    return Response({"message": "Wishlist deleted successfully"})