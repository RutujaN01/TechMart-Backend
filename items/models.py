from mongoengine import Document, StringField, IntField, FloatField, ListField, DecimalField
from decimal import Decimal
# Create your models here.
class Items(Document):
    name = StringField(required = True, max_length = 50)
    # price = DecimalField(required = True, decimal_places=2, min_value = 0)
    price = DecimalField(required = True, decimal_places=2, min_value = Decimal(0))
    description = StringField(max_length=300)
    category = StringField(max_length=20)
    
    def save(self, *args, **kwargs):
        super(Items, self).save(*args, **kwargs)

        
    meta = {
        'collection': 'items'
    }