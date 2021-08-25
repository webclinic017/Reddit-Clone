import boto3


class TokenStorage:
    """
    Represents the DynamoDB tokens table being used to store
    access and refresh tokens for the authentication service
    """
    __instance = None

    @staticmethod
    def get_instance():
        """
        Method to get the singleton instance of the TokenStorage
        class
        """
        if TokenStorage.__instance is None:
            msg = 'TokenStorage must be instantiated \
                    before using this method'
            raise Exception(msg)
        return TokenStorage.__instance

    def __init__(self, table_name, aws_region):
        if TokenStorage.__instance is not None:
            msg = 'TokenStorage has already been \
                    instantiated and is a singleton'
            raise Exception(msg)
        else:
            self._table_name = table_name
            self._aws_region = aws_region
            dynamodb = boto3.resource(
                'dynamodb', region_name=self._aws_region)
            self._tokens_table = dynamodb.Table(self._table_name)

            TokenStorage.__instance = self

    def query(self, tokenId: str, userId: str):
        """
        Method to retrieve the token with the given token and user id from
        the dynamoDB tokens table
        """
        try:
            query = self._tokens_table.get_item(
                Key={
                    'userId': userId,
                    'tokenId': tokenId
                })

            if not query['Item']:
                return None

            return query['Item']

        except Exception:
            return None

    def save_access_token(self, tokenId: str, userId: str, ipAddr: str, userAgent: str):
        """
        helper function to create a new entry in the tokens dynamoDB table
        """
        try:
            self._tokens_table.put_item(Item={
                'userId': userId,
                'tokenId': tokenId,
                'ipAddr': ipAddr,
                'userAgent': userAgent,
                'type': 'access',
                'hasBeenRevoked': False,
            })
            return True

        except Exception:
            return False

    def save_refresh_token(self, tokenId: str, userId: str, access_token_id: str, ipAddr: str, userAgent: str):
        """
        helper function to create a new entry in the tokens dynamoDB table
        """
        try:
            token = {
                'userId': userId,
                'tokenId': tokenId,
                'accessTokenId': access_token_id,
                'ipAddr': ipAddr,
                'userAgent': userAgent,
                'type': 'refresh',
                'hasBeenRevoked': False,
            }

            self._tokens_table.put_item(Item=token)
            return True

        except Exception:
            return False

    def delete(self, tokenId: str, userId: str):
        """
        helper function to delete a token from the dynamoDB tokens table
        """
        try:
            self._tokens_table.delete_item(
                Key={
                    'userId': userId,
                    'tokenId': tokenId,
                }
            )
            return True
        except Exception:
            return False
