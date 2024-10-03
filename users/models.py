from mongoengine import Document, StringField, ListField, ReferenceField
from mongoengine.fields import EmailField
from django.contrib.auth.hashers import make_password


# Create your models here.
class User(Document):
    google_id = StringField()
    username = StringField(required=True, unique=True, max_length=50)
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=100)
    roles = ListField(StringField(), default=["user"])
    # Exclude this next field from the database
    authenticated = False

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    meta = {
        'collection': 'users'
    }

    @property
    def is_staff(self):
        return 'admin' in self.roles

    @property
    def is_authenticated(self):
        return self.authenticated


class Token(Document):
    username = StringField(unique=True, required=True)
    token = StringField(required=True)

    meta = {
        'collection': 'tokens'
    }