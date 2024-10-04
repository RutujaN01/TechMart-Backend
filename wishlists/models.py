from mongoengine import Document, StringField, IntField, FloatField, ListField, DecimalField, ReferenceField, CASCADE
from django.db import models
# https://docs.mongoengine.org/tutorial.html#defining-our-documents
# 1.2.2.4. Handling deletions of references and 1.2.2.1. Posts
from users.models import User
from items.models import Items
# Create your models here.
class Wishlists(Document):
    name = StringField(required = True, unique = True, max_length = 30)
    userID = ReferenceField(User,reverse_delete_rule= CASCADE)
    item_ids = ListField(ReferenceField(Items),reverse_delete_rule= CASCADE)
    
    def save(self, *args, **kwargs):
        super(Wishlists, self).save(*args, **kwargs)

        
    meta = {
        'collection': 'wishlists'
    }