import boto3
from boto3.dynamodb.conditions import Attr
from uuid import uuid4
import os

client = boto3.client('dynamodb', region_name=os.environ.get('AWS_REGION'))
users_table_name = os.environ.get('USER_DYNAMODB_TABLE_NAME')
token_table_name = os.environ.get('TOKEN_DYNAMODB_TABLE_NAME')

dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION'))
users_table = dynamodb.Table(users_table_name)
tokens_table = dynamodb.Table(token_table_name)


def queryUserByEmail(email: str):
    """
    Helper function to retrieve the user with the given email
    address from the users DynamoDB Table
    """
    try:
        query = users_table.get_item(
            Key={
                'email': email
            })

        if not query['Item']:
            return None

        return query['Item']

    except Exception as e:
        print(f"ERROR: {e}")
        return None


def queryUsernameForUserId(userId: str):
    """
    Helper function to retrieve the user with the given email
    address from the users DynamoDB Table
    """
    try:
        query = users_table.scan(
            ProjectionExpression='username',
            FilterExpression=Attr('userId').eq(userId)
        )

        if not query or 'Items' not in query:
            return None

        return query['Items']

    except Exception:
        return None


def queryCreateNewUser(username: str, email: str, password: str):
    """
    helper function to create a new user in the dynamoDB users
    table
    """
    try:
        newUserId = uuid4().hex
        users_table.put_item(Item={
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


def queryTokenByUserId(userId: str, ipAddr: str):
    """
    helper function to retrieve the token with the given user id from
    the dynamoDB tokens table
    """
    try:
        query = tokens_table.get_item(
            Key={
                'userId': userId,
                'ipAddr': ipAddr
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
        tokens_table.put_item(Item={
            'userId': userId,
            'ipAddr': ipAddr,
            'userAgent': userAgent,
            'token': token,
        })
        return True

    except Exception:
        return False


def queryDeleteToken(userId: str, ipAddr: str):
    """
    helper function to delete a token from the dynamoDB tokens table
    """
    try:
        tokens_table.delete_item(
            Key={
                'userId': userId,
                'ipAddr': ipAddr
            }
        )
        return True
    except Exception:
        return False
