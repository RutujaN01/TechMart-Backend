from functools import wraps

from django.http import JsonResponse
from mongoengine import DoesNotExist
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


def admin_route(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Extract the JWT token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Unauthorized: No token provided"}, status=401)

        try:
            # Validate the JWT token and extract the user ID
            access_token = AccessToken(token.split(' ')[1])
            user_id = access_token['user_id']
        except Exception as e:
            return JsonResponse({"error": f"Unauthorized: Invalid token - {str(e)}"}, status=401)

        try:
            # Fetch the user from the database
            user = User.objects.get(id=user_id)
        except DoesNotExist:
            return JsonResponse({"error": "Unauthorized: Invalid user_id"}, status=401)

        # Check if the user is an admin
        if "admin" in user.roles:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "Unauthorized: Insufficient permissions"}, status=403)

    return wrapper
