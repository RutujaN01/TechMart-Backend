from functools import wraps

from bson import ObjectId
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from mongoengine import DoesNotExist

from users.models import User


def admin_route(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Validate and authenticate the user
        print(request.headers)
        user_id = request.headers.get('Requester-Id')
        # user_id = ObjectId(user_id)
        # print(user_id)
        if not user_id:
            return JsonResponse({"error": "Unauthorized: No user_id provided"}, status=401)

        try:
            user = User.objects().get(id=user_id)
        except DoesNotExist:
            return JsonResponse({"error": "Unauthorized: Invalid user_id"}, status=401)

        # Check if the user is an admin
        if "admin" in user.roles:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "Unauthorized: Insufficient permissions"}, status=403)

    return wrapper