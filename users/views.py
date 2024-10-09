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
    access_token = str(refresh.access_token)

    # Check if a token already exists for the user
    token = Token.objects(user=user).first()
    if token:
        # Update the existing token
        token.token = access_token
        token.save()
    else:
        # Create a new token
        new_token = Token(user=user, token=access_token, username=user.username)
        new_token.save()

    # Exclude the password hash
    user_data = UserSerializer(user).data
    user_data.pop("password")

    # Return the refresh token, access token, and user data
    return Response({
        "refresh": str(refresh),
        "access": access_token,
        "user": user_data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Find the user with the provided username
    username = request.user.username
    user = User.objects(username=username).first()

    # Check if the user exists
    if user is None:
        return Response({"error": "User not found"}, status=404)

    # Remove the token from the database
    token = Token.objects(user=user).first()
    if token:
        token.delete()
        return Response({"message": "Logout successful"})
    else:
        return Response({"error": "Token not found"}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    # Body will contain the username and password of the user to be deleted and the refresh token
    user_data = request.data
    user = User.objects(username=user_data["username"]).first()

    if not user:
        return Response({"error": "User not found"}, status=404)

    # Check if the user is an admin
    if 'admin' in user.roles:
        return Response({"error": "Cannot delete an admin"}, status=403)

    # Check if the user is trying to delete themselves
    if user.username != request.user.username and 'admin' not in request.user.roles:
        return Response({"error": "Cannot delete another user"}, status=403)

    # Check if the password is correct if the user is not an admin
    if 'admin' not in request.user.roles and not check_password(user_data["password"], user.password):
        return Response({"error": "Invalid password"}, status=401)

    # Delete the user
    user.delete()

    return Response({"message": "User deleted"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    user_data = UserSerializer(user).data
    # Exclude the password hash
    user_data.pop("password")
    return Response({"data": user_data})


@api_view(['GET', 'PUT'])
@admin_route
def get_users(request):
    # Handle the PUT request
    if request.method == 'PUT':

        # Admin will send in a list of users to add
        users = request.data["users"]
        for user in users:
            print(dict(user))
            user = User(**user)
            user.save()
        return Response({"message": "Users added"})

    # Handle the GET request
    users = User.objects()
    users_data = UserSerializer(users, many=True).data
    return Response({"data": users_data})
