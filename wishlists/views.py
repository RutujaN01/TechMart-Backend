from django.shortcuts import render
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

