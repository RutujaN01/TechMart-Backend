from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from mongoengine.errors import NotUniqueError

from decorators import admin_route
from .models import User
from .serializers import UserSerializer


# Create your views here.
# Establish that the view takes a POST request
@api_view(['POST'])
def create_user(request):
    # Extract the user data from the request and create a new user
    user_data = request.data
    user = User(**user_data)

    # Save the user to the database
    try:
        user.save()
    except NotUniqueError:
        # If the user already exists, return an error
        return Response({"error": "User already exists with that information"}, status=400)
    except Exception as e:
        # If there is an error saving the user, return the
        return Response({"error": str(e)}, status=400)

    # Serialize the user data and return it
    user_data = UserSerializer(user).data
    return Response({"data": user_data})


