import unittest
import os
from utils.tokens import JsonWebToken
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


class MockRSAKeys:
    """
    Helper class for generating RSA public/private key pairs to be used
    when testing the JsonWebToken class
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
    """Test JsonWebToken Class"""

    @classmethod
    def setUpClass(cls):
        """instantiate JsonWebToken singleton before running tests"""
        public_key, private_key = MockRSAKeys.get_key_pair()
        JsonWebToken(public_key, private_key)

    def test_can_get_singleton_instance(self):
        """Test that we can get the singleton instance for the JsonWebToken"""
        first_instance = JsonWebToken.get_instance()
        self.assertIsNotNone(first_instance)

        second_instance = JsonWebToken.get_instance()
        self.assertIsNotNone(second_instance)

    def test_instance_is_singleton_instance(self):
        """Test that the singleton instances are the same"""
        first_instance = JsonWebToken.get_instance()
        second_instance = JsonWebToken.get_instance()

        self.assertIs(first_instance, second_instance)

    def test_can_create_a_token(self):
        """Test that we can create a JWT"""

        tokenManager = JsonWebToken.get_instance()
        payload = payload = {'data': 'test token data'}
        timeToLiveInSeconds = 1500

        tokenId, token = tokenManager.create(payload, timeToLiveInSeconds)
        self.assertIsNotNone(tokenId, 'Could not create token')
        self.assertIsNotNone(token, 'Could not create token')

    def test_can_decode_token_after_creation(self):
        """Test that JWT can be decoded to get original data"""

        tokenManager = JsonWebToken.get_instance()
        payload = {'data': 'test token data'}
        timeToLiveInSeconds = 1500

        tokenId, token = tokenManager.create(payload, timeToLiveInSeconds)
        self.assertIsNotNone(token, 'Could not create token')

        decoded_payload = tokenManager.decode(token)
        msg = 'Decoded payload data does not match original payload'
        self.assertEqual(payload['data'], decoded_payload['data'], msg)

        msg = 'Decoded payload tokenId does not match original payload'
        self.assertEqual(tokenId, decoded_payload['tokenId'], msg)

    def test_can_deconde_without_verification(self):
        """
        Test that JWT can be decoded without verification
        to get original data
        """
        tokenManager = JsonWebToken.get_instance()
        payload = {'data': 'test token data'}
        # set TTL to -100 so that it is already expired
        timeToLiveInSeconds = -100

        tokenId, token = tokenManager.create(payload, timeToLiveInSeconds)
        self.assertIsNotNone(token, 'Could not create token')

        invalid_payload = tokenManager.decode(token)
        msg = 'Token should not be able to be decoded with verification'
        self.assertIsNone(invalid_payload, msg)

        valid_payload = tokenManager.decode_without_verification(token)
        msg = 'Decoded payload data does not match original payload'
        self.assertEqual(payload['data'], valid_payload['data'], msg)

        msg = 'Decoded payload tokenId does not match original payload'
        self.assertEqual(tokenId, valid_payload['tokenId'], msg)


if __name__ == '__main__':
    unittest.main(verbosity=2)
