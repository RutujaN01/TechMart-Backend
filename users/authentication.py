from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from mongoengine.errors import DoesNotExist
from users.models import User, Token
from bson import ObjectId

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None

        try:
            access_token = AccessToken(token.split(' ')[1])
            user_id = access_token['user_id']

            user = User.objects.get(id=ObjectId(user_id))

            token_from_db = Token.objects.get(user=user)

            # The token passed in will be "Bearer <token>" where token is the access token
            if token_from_db.token != token.split(' ')[1]:
                raise AuthenticationFailed('Invalid token')
            user.authenticated = True
            return user, None
        except (DoesNotExist, KeyError):
            raise AuthenticationFailed('Invalid token or user does not exist')