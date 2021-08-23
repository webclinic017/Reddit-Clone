import jwt
from datetime import datetime, timedelta
import json
from typing import Dict
from uuid import uuid4


class JsonWebToken:
    __instance = None

    @staticmethod
    def get_instance():
        """Method to get the singleton instance of the JsonWebToken class"""
        if JsonWebToken.__instance is None:
            msg = 'JsonWebToken must be instantiated before using this method'
            raise Exception(msg)
        return JsonWebToken.__instance

    def __init__(self, public_key, private_key):
        if JsonWebToken.__instance is not None:
            msg = 'JsonWebToken has already been \
                    instantiated and is a singleton'
            raise Exception(msg)
        else:
            self._private_key = private_key
            self._public_key = public_key
            JsonWebToken.__instance = self

    def get_public_key(self):
        """Method to get the public key for the token manager"""
        return self._public_key

    def _get_private_key(self):
        """Method to get the private key for the token manager"""
        return self._private_key

    def create(self, payload: Dict, timeToLiveInSeconds: int):
        """
        Method to create a JSON Web Token containing the Id of
        a user
        """
        try:
            # create a token id and add to the payload
            tokenId = uuid4().hex
            payload['tokenId'] = tokenId

            token = jwt.encode(
                {
                    'payload': json.dumps(payload),
                    "exp": datetime.utcnow() + timedelta(
                        seconds=timeToLiveInSeconds)
                },
                self._private_key.encode(),
                algorithm="RS256"
            )
            return tokenId, token
        except Exception as e:
            print(e)
            return None, None

    def decode(self, token: str) -> Dict:
        """
        Function to decode and return the Id of a user contained in
        a JSON Web Token
        """
        try:
            payload = jwt.decode(
                token, self._public_key.encode(), algorithms=["RS256"])

            if payload is None or 'payload' not in payload:
                return None

            return json.loads(payload['payload'])
        except Exception:
            return None

    def decode_without_verification(self, token: str) -> Dict:
        """
        Function to decode and return the Id of a user contained in
        a JSON Web Token
        """
        try:
            payload = jwt.decode(
                token,
                self._public_key.encode(),
                algorithms=["RS256"],
                options={'verify_signature': False})
            if not payload or 'payload' not in payload:
                return None

            return json.loads(payload['payload'])
        except Exception:
            return None
