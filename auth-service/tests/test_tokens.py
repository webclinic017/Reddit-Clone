import unittest
import os
from utils.tokens import TokenManager
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


class MockRSAKeys:
    """
    Helper class for generating RSA public/private key pairs to be used
    when testing the TokenManager class
    """

    @staticmethod
    def get_key_pair():
        # generate private/public key pair
        key = rsa.generate_private_key(backend=default_backend(),
                                       public_exponent=65537,
                                       key_size=2048)

        # get private key in PEM container format
        pem = key.private_bytes(encoding=serialization.Encoding.PEM,
                                format=serialization.PrivateFormat.TraditionalOpenSSL,
                                encryption_algorithm=serialization.NoEncryption())

        public_key = key.public_key().public_bytes(encoding=serialization.Encoding.PEM,
                                                   format=serialization.PublicFormat.SubjectPublicKeyInfo)

        # decode to printable strings
        private_key_str = pem.decode('utf-8')
        public_key_str = public_key.decode('utf-8')

        return public_key_str, private_key_str


class TestMockRSAKeys(unittest.TestCase):
    """Test MockRSAKeys Class"""

    def test_can_generate_key_pair(self):
        public_key, private_key = MockRSAKeys.get_key_pair()

        self.assertIsNotNone(public_key, 'Public key is None')
        self.assertIsNotNone(private_key, 'Private Key is None')


class TestTokenManager(unittest.TestCase):
    """Test TokenManager Class"""

    @classmethod
    def setUpClass(cls):
        """Set environment variables before running tests"""
        public_key, private_key = MockRSAKeys.get_key_pair()
        os.environ['TOKEN_PRIVATE_KEY'] = private_key
        os.environ['TOKEN_PUBLIC_KEY'] = public_key

    def test_can_get_singleton_instance(self):
        """Test that we can get the singleton instance for the TokenManager"""
        first_instance = TokenManager.get_instance()
        self.assertIsNotNone(first_instance)

        second_instance = TokenManager.get_instance()
        self.assertIsNotNone(second_instance)

    def test_instance_is_singleton_instance(self):
        """Test that the singleton instances are the same"""
        first_instance = TokenManager.get_instance()
        second_instance = TokenManager.get_instance()

        self.assertIs(first_instance, second_instance)

    def test_token_manager_load_private_key(self):
        """Test that the TokenManager loads private key environment variable"""

        # ensure that the TOKEN_PRIVATE_KEY environment variable is set
        env_private_key = os.environ.get('TOKEN_PRIVATE_KEY', None)
        msg = 'TOKEN_PRIVATE_KEY environment variable has not been set'
        self.assertIsNotNone(env_private_key, msg)

        # Get the token manager instance
        tokenManager = TokenManager.get_instance()

        # get the private key from the instance
        private_key = tokenManager._get_private_key()
        msg = f'self._private_token is None, but should be {env_private_key}'
        self.assertIsNotNone(private_key)

        # check that keys match
        msg = 'TokenManager private key does not match environment variable'
        self.assertEqual(env_private_key, private_key)

    def test_token_manager_load_public_key(self):
        """Test that the TokenManager loads public key environment variable"""

        # ensure that the TOKEN_PUBLIC_KEY environment variable is set
        env_public_key = os.environ.get('TOKEN_PUBLIC_KEY', None)
        msg = 'TOKEN_PUBLIC_KEY environment variable has not been set'
        self.assertIsNotNone(env_public_key, msg)

        # Get the token manager instance
        tokenManager = TokenManager.get_instance()

        # get the public key from the instance
        public_key = tokenManager.get_public_key()
        msg = f'self._public_token is None, but should be {env_public_key}'
        self.assertIsNotNone(public_key)

        # check that keys match
        msg = 'TokenManager public key does not match environment variable'
        self.assertEqual(env_public_key, public_key)

    def test_can_create_a_token(self):
        """Test that we can create a JWT"""

        tokenManager = TokenManager.get_instance()
        payload = "test token data"
        timeToLiveInSeconds = 1500

        token = tokenManager.create(payload, timeToLiveInSeconds)
        self.assertIsNotNone(token, 'Could not create token')

    def test_can_decode_token_after_creation(self):
        """Test that JWT can be decoded to get original data"""

        tokenManager = TokenManager.get_instance()
        payload = "test token data"
        timeToLiveInSeconds = 1500

        token = tokenManager.create(payload, timeToLiveInSeconds)
        self.assertIsNotNone(token, 'Could not create token')

        decoded_payload = tokenManager.decode(token)
        msg = 'Decoded payload does not match original payload'
        self.assertEqual(payload, decoded_payload, msg)


if __name__ == '__main__':
    unittest.main(verbosity=2)
