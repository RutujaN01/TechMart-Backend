from mongoengine import Document, StringField, IntField, FloatField, ListField

# Create your models here.
class Itemss(Document):
    ID = IntField()
    name = StringField()
    description = StringField()
    category = StringField()
    

    meta = {
        'collection': 'Items'
    }