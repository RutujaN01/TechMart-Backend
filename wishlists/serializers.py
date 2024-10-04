from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Wishlists

class WishlistsSerializer(DocumentSerializer):
    class Meta:
        model = Items
        fields = '__all__'