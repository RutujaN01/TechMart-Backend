from django.contrib.auth.hashers import check_password
from mongoengine.errors import NotUniqueError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from decorators import admin_route
from .models import User, Token
from .serializers import UserSerializer


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

    # Store the refresh token in the database
    Token(username=user.username, token=str(refresh)).save()

    # Exclude the password hash
    user_data = UserSerializer(user).data
    user_data.pop("password")

    # Return the refresh token, access token, and user data
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": user_data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request, username):
    # Extract the refresh token from the request
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response({"error": "Refresh token not provided"}, status=400)

    # Find the user with the provided username
    user = User.objects(username=username).first()

    # Check if the user exists
    if user is None:
        return Response({"error": "User not found"}, status=404)

    # Remove the token from the database
    token = Token.objects(username=user['username']).first()
    if token:
        token.delete()
        return Response({"message": "Logout successful"})
    else:
        return Response({"error": "Token not found"}, status=404)
