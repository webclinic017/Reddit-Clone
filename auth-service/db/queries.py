import boto3
from uuid import uuid4
import os

client = boto3.client('dynamodb', region_name=os.environ.get('AWS_REGION'))
users_table = os.environ.get('USER_DYNAMODB_TABLE_NAME')
token_table = os.environ.get('TOKEN_DYNAMODB_TABLE_NAME')


def queryUserByEmail(email: str):
    """
    Helper function to retrieve the user with the given email
    address from the users DynamoDB Table
    """
    try:
        query = client.get_item(
            TableName=users_table,
            Key={
                'email': {'S': email}
            })

        if not query['Item']:
            return None

        return query['Item']

    except Exception as e:
        print(f"ERROR: {e}")
        return None


def queryCreateNewUser(username: str, email: str, password: str):
    """
    helper function to create a new user in the dynamoDB users
    table
    """
    try:
        newUserId = uuid4().hex
        client.put_item(TableName=users_table, Item={
            'userId': {'S': newUserId},
            'email': {'S': email},
            'username': {'S': username},
            'password': {'S': password},
        })

        return newUserId
    except Exception:
        return None


def queryTokenByUserId(userId: str):
    """
    helper function to retrieve the token with the given user id from
    the dynamoDB tokens table
    """
    try:
        query = client.get_item(
            TableName=token_table,
            Key={
                'userId': {'S': userId}
            })

        if not query['Item']:
            return None

        return query['Item']

    except Exception:
        return None


def queryCreateNewToken(userId: str, ipAddr: str, userAgent: str, token: str):
    """
    helper function to create a new entry in the tokens dynamoDB table
    """
    try:
        client.put_item(TableName=token_table, Item={
            'userId': {'S': userId},
            'ipAddr': {'S': ipAddr},
            'userAgent': {'S': userAgent},
            'token': {'S': token},
        })
        return True

    except Exception:
        return False


def queryDeleteToken(userId: str):
    """
    helper function to delete a token from the dynamoDB tokens table
    """
    try:
        client.delete_item(
            TableName=token_table,
            Key={
                'userId': {'S': userId}
            }
        )
        return True
    except Exception:
        return False
