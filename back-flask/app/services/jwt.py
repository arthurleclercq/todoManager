import jwt
from app import config

def decodeToken(token):
    try:
        return (jwt.decode(token,config.API_KEY,algorithms=["HS256"])["user"])
    except Exception as e:
        print(e)
        return None
    
def encodeToken(user):
    return jwt.encode({"user":user},config.API_KEY,algorithm="HS256")