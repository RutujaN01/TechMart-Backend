from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Items

class ItemsSerializer(DocumentSerializer):
    class Meta:
        model = Items
        fields = '__all__'