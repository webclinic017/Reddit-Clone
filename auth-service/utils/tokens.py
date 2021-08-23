import jwt
from datetime import datetime, timedelta
import os


class TokenManager:
    __instance = None

    @staticmethod
    def get_instance():
        """Method to get the singleton instance of the TokenManager class"""
        if TokenManager.__instance is None:
            TokenManager()
        return TokenManager.__instance

    def __init__(self):
        if TokenManager.__instance is not None:
            msg = 'TokenManager has already been \
                    instantiated and is a singleton'
            raise Exception(msg)
        else:
            self._private_key = os.environ.get('TOKEN_PRIVATE_KEY')
            self._public_key = os.environ.get('TOKEN_PUBLIC_KEY')
            TokenManager.__instance = self

    def get_public_key(self):
        """Method to get the public key for the token manager"""
        return self._public_key

    def _get_private_key(self):
        """Method to get the private key for the token manager"""
        return self._private_key

    def create(self, payload: str, timeToLiveInSeconds: int):
        """
        Method to create a JSON Web Token containing the Id of
        a user
        """
        try:
            token = jwt.encode(
                {
                    'payload': payload,
                    "exp": datetime.utcnow() + timedelta(
                        seconds=timeToLiveInSeconds)
                },
                self._private_key.encode(),
                algorithm="RS256"
            )
            return token
        except Exception as e:
            print(e)
            return None

    def decode(self, token: str):
        """
        Function to decode and return the Id of a user contained in
        a JSON Web Token
        """
        try:
            payload = jwt.decode(
                token, self._public_key.encode(), algorithms=["RS256"])
            if not payload or 'payload' not in payload:
                return None

            return payload['payload']
        except Exception:
            return None
