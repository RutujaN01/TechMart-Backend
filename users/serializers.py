from rest_framework_mongoengine.serializers import DocumentSerializer

from .models import User


class UserSerializer(DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'
