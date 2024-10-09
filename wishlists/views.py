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
