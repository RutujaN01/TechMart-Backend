from rest_framework_mongoengine.serializers import DocumentSerializer

from items.serializers import ItemsSerializer
from users.serializers import UserSerializer
from .models import Wishlists


class WishlistsSerializer(DocumentSerializer):
    user = UserSerializer()
    items = ItemsSerializer(many=True)

    class Meta:
        model = Wishlists
        fields = '__all__'
