import jwt
from dotenv import dotenv_values

config = dotenv_values('.env')
public_key = config['TOKEN_PUBLIC_KEY']


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
