import jwt
from config.settings import JWT_SECRET_KEY

def auth_validate_check(request, user_id):
    try:
        access_token = request.COOKIES['access_token']
        byte_access_token = access_token.encode('utf-8')
        payload = jwt.decode(byte_access_token, JWT_SECRET_KEY, algorithm='HS256')
        if payload['user_id'] == user_id:
            return True
        else:
            return False
    except:
        return False