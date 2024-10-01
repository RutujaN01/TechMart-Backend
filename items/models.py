from mongoengine import Document, StringField, IntField, FloatField, ListField

# Create your models here.
class Itemss(Document):
    ID = IntField()
    name = StringField()
    price = DecimalField(precision=2)
    description = StringField()
    category = StringField()
    

    meta = {
        'collection': 'Items'
    }