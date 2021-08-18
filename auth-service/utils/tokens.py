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
                "exp": datetime.utcnow() + timedelta(seconds=1500)
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


def isRequestFromSavedTokenHolder(request, token):
    """
    Function takes a flask request object and a token database entry
    and checks that the request appears to come from the same device
    and user agent
    """
    hasSameIpAddr = token['ipAddr'] == request.remote_addr
    hasSameUserAgent = token['userAgent'] == request.user_agent.string

    return hasSameIpAddr and hasSameUserAgent
