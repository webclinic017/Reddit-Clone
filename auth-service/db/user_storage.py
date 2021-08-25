import boto3
from uuid import uuid4


class UserStorage:
    """
    Represents the DynamoDB tokens table being used to store
    access and refresh tokens for the authentication service
    """
    __instance = None

    @staticmethod
    def get_instance():
        """
        Method to get the singleton instance of the UserStorage
        class
        """
        if UserStorage.__instance is None:
            msg = 'UserStorage must be instantiated \
                    before using this method'
            raise Exception(msg)
        return UserStorage.__instance

    def __init__(self, table_name, aws_region):
        if UserStorage.__instance is not None:
            msg = 'UserStorage has already been \
                    instantiated and is a singleton'
            raise Exception(msg)
        else:
            self._table_name = table_name
            self._aws_region = aws_region
            dynamodb = boto3.resource(
                'dynamodb', region_name=self._aws_region)
            self._users_table = dynamodb.Table(self._table_name)

            UserStorage.__instance = self

    def query_by_email(self, email: str):
        """
        Method to retrieve the user with the given email
        """
        try:
            query = self._users_table.get_item(
                Key={
                    'email': email
                })

            if not query['Item']:
                return None

            return query['Item']

        except Exception:
            return None

    def create(self, username: str, email: str, password: str):
        """
        helper function to create a new user in the dynamoDB users
        table
        """
        try:
            newUserId = uuid4().hex
            self._users_table.put_item(Item={
                'userId': newUserId,
                'email': email,
                'username': username,
                'password': password,
            })

            newUser = {
                "userId": newUserId,
                "username": username,
                "email": email
            }

            return newUser
        except Exception:
            return None
