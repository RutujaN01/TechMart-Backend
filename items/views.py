from django.contrib.auth.hashers import check_password
from mongoengine.errors import NotUniqueError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)


from decimal import Decimal

from decorators import admin_route
from users.models import User, Token
from .models import Items
from .serializers import ItemsSerializer


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_items(request):
    items = Items.objects.all()
    items_data = ItemsSerializer(items, many=True)
    return Response(items_data.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getItem(request):
    item_id = request.GET.get('id')
    item = Items.objects(id=item_id).first()
    
    item_data = ItemsSerializer(item)
    return Response(item_data.data)


@api_view(['GET'])
def getItemByName(request, item_name):
    print(item_name)
    if not item_name:
        return Response({"error": "Item name is required"}, status=400)  

    item = Items.objects(name__icontains = item_name).first()
    if not item:
        return Response({"error": "Item not found"}, status=404)  

    item_data = ItemsSerializer(item)
    return Response(item_data.data)

# https://docs.mongoengine.org/guide/querying.html
@api_view(['GET'])
def getItemsByCat(request):
    item_cat = request.GET.get('category')
    items = Items.objects.filter(category__icontains = item_cat)
    # print(item_cat)
    print(items)
    
    items_data = ItemsSerializer(items, many = True)
    return Response(items_data.data)




@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def delete_item(request):
    # item_data = request.data
    # item = Items.objects(name=item_data["name"]).first()
    item_id = request.data.get('id')
    item = Items.objects(id=item_id).first()

    if not item:
        return Response({"error": "Item not found"}, status=404)
    
    item.delete()

    return Response({"message": "Item deleted"})



@api_view(['POST'])
def create_item(request):
    item_data = request.data
    item = Items(**item_data)
    # print(item.price)
    # print(item)
    
    try:
        item.save()
    except NotUniqueError:
        return Response({"error": "Item already exists with that information"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    # Serialize the item data and return it
    item_data = ItemsSerializer(item).data
    return Response({"data": item_data})




@api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
def update_item(request):
    item_data = request.data
    logger.info(f"Updating item with data: {item_data}")

    item = Items.objects(id=item_data.get("id")).first()
    if not item:
        logger.warning("Item not found")
        return Response({"error": "Item not found"}, status=404)

    item_info = ItemsSerializer(item, data=request.data, partial=True)
    if item_info.is_valid():
        item_info.save()
        logger.info("Item updated successfully")
        return Response(item_info.data, status=200)
    else:
        logger.error(f"Validation errors: {item_info.errors}")
        return Response(item_info.errors, status=400)



# search name, search by category objects.fileter 