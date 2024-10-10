# from django.contrib.auth.hashers import check_password
from mongoengine.errors import NotUniqueError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from decorators import admin_route
from users.models import User, Token
from .models import Items
from .serializers import ItemsSerializer


# https://docs.mongoengine.org/guide/querying.html
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_items(request):
    items = Items.objects.all()
    items_data = ItemsSerializer(items, many=True)
    return Response(items_data.data)

