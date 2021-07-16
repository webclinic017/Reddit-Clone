import jwt
from datetime import datetime, timedelta
import os

private_key = os.environ.get('TOKEN_PRIVATE_KEY')
public_key = os.environ.get('TOKEN_PUBLIC_KEY')


def createJWT(userId: str):
    """
    Function to create a JSON Web Token containing the Id of
    a user
    """
    try:
        token = jwt.encode(
            {
                'id': userId,
                "exp": datetime.utcnow() + timedelta(seconds=900)
            },
            private_key.encode(),
            algorithm="RS256"
        )
        return token
    except Exception:
        return None


def getUserIdFromToken(token):
    """
    Function to decode and return the Id of a user contained in
    a JSON Web Token
    """
    try:
        payload = jwt.decode(
            token, public_key.encode(), algorithms=["RS256"])
        if not payload or 'id' not in payload:
            return None

        return payload['id']
    except Exception:
        return None
