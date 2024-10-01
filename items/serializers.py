from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Itemss

class ItemsSerializer(DocumentSerializer):
    class Meta:
        model = Itemss
        fields = '__all__'