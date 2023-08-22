from jose import jwt
from django.conf import settings

from jose.exceptions import ExpiredSignatureError, JWTError
class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.META.get('HTTP_USER_ID')

        request.user_id = user_id if user_id else None
        
        response = self.get_response(request)
        return response

class UserIDJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        
        if authorization_header and authorization_header.startswith('Bearer '):
            token = authorization_header.split(' ')[1]
            
            try:
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token.get('user_id')
            except ExpiredSignatureError:
                user_id = None
            except JWTError:
                user_id = None
        else:
            user_id = None

        request.user_id = user_id

        response = self.get_response(request)
        return response
