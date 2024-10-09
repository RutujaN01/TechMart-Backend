from mongoengine import Document, StringField, ListField, ReferenceField, CASCADE, \
    BooleanField

from items.models import Items
# https://docs.mongoengine.org/tutorial.html#defining-our-documents
# 1.2.2.4. Handling deletions of references and 1.2.2.1. Posts
from users.models import User


# Create your models here.
class Wishlists(Document):
    name = StringField(required=True, unique_with='user', max_length=50)
    user = ReferenceField(User, unique_with='name', reverse_delete_rule=CASCADE)
    items = ListField(ReferenceField(Items, reverse_delete_rule=CASCADE), default=list)
    isPublic = BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(Wishlists, self).save(*args, **kwargs)

    meta = {
        'collection': 'wishlists'
    }
