from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.
from rest_framework.response import Response

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

@api_view(['GET'])
def hello_user_with_name(request, name):
    return Response(f'Hello, {name}!')