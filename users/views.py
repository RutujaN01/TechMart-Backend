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
@api_view(['GET'])
@admin_route
def test(request):
    # Create a test user
    test_user = User(username="John", email="test@gmail.com", password="test")
    try:
        test_user.save()
    except NotUniqueError:
        return Response({"error": "User already exists"}, status=400)

    # Find the test user with a query
    test_user = User.objects().get(id=test_user.id)
    # Serialize and return the test user
    return_user_data = UserSerializer(test_user).data

    # Clean up
    test_user.delete()

    return Response({"data": return_user_data})

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


@api_view(['POST'])
def login(request):
    # Extract the login data from the request
    login_data = request.data

    # Find the user with the provided username
    user = User.objects(username=login_data["username"]).first()

    # Check if the user exists and the password is correct
    if user is None or not check_password(login_data["password"], user.password):
        return Response({"error": "Invalid credentials"}, status=401)

    # If the user exists and the password is correct, create a refresh token
    refresh = RefreshToken.for_user(user)

    # Exclude the password hash
    user_data = UserSerializer(user).data
    user_data.pop("password")

    # Return the refresh token, access token, and user data
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": user_data
    })

