from mongoengine.errors import NotUniqueError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from items.models import Items
from items.serializers import ItemsSerializer
from users.models import User
from .models import Wishlists
from .serializers import WishlistsSerializer


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
def get_wishlist_by_id(request, wishlist_id):
    # Extract the wishlist from the database
    wishlist = Wishlists.objects(id=wishlist_id).first()
    print(request.user)
    # If the wishlist does not exist, return an error
    if wishlist is None:
        return Response({"error": "Wishlist does not exist"}, status=404)

    # If the user is not the owner of the wishlist and the wishlist is not public, return an error
    if not request.user.is_staff:
        del wishlist.user.password
        if wishlist.user != request.user and not wishlist.isPublic:
            return Response({"error": "You do not have permission to view this wishlist"}, status=403)


    # Serialize the wishlist data and return it
    wishlist_data = WishlistsSerializer(wishlist).data
    return Response({"data": wishlist_data})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_item_to_wishlist(request):
    # Extract the wishlist and item IDs from the request
    item_id = request.data["item_id"]
    wishlist_id = request.data["wishlist_id"]
    # Find the wishlist by ID
    wishlist = Wishlists.objects(id=wishlist_id).first()

    # If the wishlist does not exist, return an error
    if wishlist is None:
        return Response({"error": "Wishlist does not exist"}, status=404)

    # If the user is not the owner of the wishlist, return an error
    if wishlist.user != request.user and not request.user.is_staff:
        return Response({"error": "You do not have permission to update this wishlist"}, status=403)

    # Find the item by ID
    item = Items.objects(id=item_id).first()

    # If the item does not exist, return an error
    if item is None:
        return Response({"error": "Item does not exist"}, status=404)

    if item in wishlist.items:
        # Remove the item from the wishlist
        wishlist.items.remove(item)
    else:
        # Add the item to the wishlist
        wishlist.items.append(item)

    # Save the wishlist
    wishlist.save()

    # Serialize the wishlist data and return it
    wishlist_data = WishlistsSerializer(wishlist).data
    return Response({"data": wishlist_data})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_wishlist(request):
    # Extract the wishlist data from the request
    wishlist_id = request.data["wishlist_id"]
    wishlist_data = request.data

    # Remove it so that Mongoengine doesn't try to update it in the Document
    wishlist_data.pop("wishlist_id")

    # If wishlist_data has nothing, return an error
    if not wishlist_data:
        return Response({"error": "No data provided to update wishlist"}, status=400)

    # Find the wishlist by ID
    wishlist = Wishlists.objects(id=wishlist_id).first()

    if wishlist is None:
        return Response({"error": "Wishlist does not exist"}, status=404)

    # If the user is not the owner of the wishlist, return an error
    if wishlist.user != request.user and not request.user.is_staff:
        return Response({"error": "You do not have permission to update this wishlist"}, status=403)

    # Update the wishlist data user to be the user object
    if "user" in wishlist_data:
        user = User.objects(id=wishlist_data["user"]).first()
        if user is None:
            return Response({"error": "User does not exist"}, status=404)
        wishlist_data["user"] = user

    # Validate the items in the wishlist
    if "items" in wishlist_data:
        items = []
        for item_id in wishlist_data["items"]:
            item = Items.objects(id=item_id).first()
            if item is None:
                return Response({"error": "Item does not exist"}, status=404)
            items.append(item)
        wishlist_data["items"] = items

    # Update the wishlist data
    wishlist.update(**wishlist_data)

    # Ensure that changes from the database are reflected in the object
    wishlist.reload()

    # Serialize the wishlist data and return it
    wishlist_data = WishlistsSerializer(wishlist).data
    return Response({"data": wishlist_data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_wishlist(request):
    # Extract the wishlist ID from the request
    wishlist_id = request.data["wishlist_id"]

    # Find the wishlist by ID
    wishlist = Wishlists.objects(id=wishlist_id).first()

    # If the wishlist does not exist, return an error
    if wishlist is None:
        return Response({"error": "Wishlist does not exist"}, status=404)

    # If the user is not the owner of the wishlist, return an error
    if wishlist.user != request.user and not request.user.is_staff:
        return Response({"error": "You do not have permission to delete this wishlist"}, status=403)

    # Delete the wishlist
    wishlist.delete()

    return Response({"message": "Wishlist deleted successfully"})
