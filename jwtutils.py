""" THIS FILE IS FOR CREATION AND VERIFICATION OF JWT """

import jwt
import datetime
from envfile import SECRET_KEY

# Create JWT Token
def create_jwt(user_id, email):
    token = jwt.encode({
        "id": user_id,
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=5)
    }, SECRET_KEY, algorithm="HS256")

    return token


# Decode / Verify JWT
def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return None
