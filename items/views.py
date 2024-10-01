from django.shortcuts import render

# Create your views here.
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# from .models import Itemss
# from .serializers import ItemsSerializer


# @api_view(['GET'])
# def hello_world(request):
#     items = Itemss()
#     items.save()

#     items = Itemms.objects.first()
#     print(items.name)
#     return Response({"data": ItemsSerializer(items).data})


# @api_view(['GET'])
# def hello_user_with_name(request, name):
#     return Response(f'Hello, {name}!')