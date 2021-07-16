import boto3
from boto3.dynamodb.conditions import Attr
import os

upvotes_table_name = os.environ.get('UPVOTES_DYNAMODB_TABLE_NAME')
downvotes_table_name = os.environ.get('DOWNVOTES_DYNAMODB_TABLE_NAME')

dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION'))
upvotes_table = dynamodb.Table(upvotes_table_name)
downvotes_table = dynamodb.Table(downvotes_table_name)


def queryAddUpvoteToPost(postId, userId):
    """
    Function to create an upvote for the given post from the given user
    """
    try:
        item = {
            'postId': postId,
            'userId': userId
        }

        upvotes_table.put_item(Item=item)
        return item
    except Exception:
        return None


def queryGetUpvoteForPost(postId, userId):
    """
    Function to retrive an upvote with the given postId and userId
    """
    try:
        query = upvotes_table.get_item(
            Key={
                "postId": postId,
                "userId": userId
            }
        )

        if not query['Item']:
            return None

        return query['Item']

    except Exception as e:
        print(f"ERROR: {e}")
        return None


def queryDeleteUpvoteForPost(postId, userId):
    """
    Function to delete an upvote with the given postId and userId
    """
    try:
        upvotes_table.delete_item(Key={
            'postId': postId,
            'userId': userId
        })
        return True
    except Exception:
        return False


def queryGetUpvotesCountForPost(postId):
    """
    Function to retrieve the total count of upvotes for a given post
    """
    try:
        query = upvotes_table.scan(
            FilterExpression=Attr('postId').eq(postId),
            Select="COUNT"
        )

        if query is None or 'Count' not in query:
            return None

        return query['Count']

    except Exception as e:
        print(f"ERROR: {e}")
        return None


def queryAddDownvoteToPost(postId, userId):
    """
    Function to create a downvote for the given post from the given user
    """
    try:
        item = {
            'postId': postId,
            'userId': userId
        }

        downvotes_table.put_item(Item=item)
        return item
    except Exception:
        return None


def queryGetDownvoteForPost(postId, userId):
    """
    Function to retrive a downvote with the given postId and userId
    """
    try:
        query = downvotes_table.get_item(
            Key={
                "postId": postId,
                "userId": userId
            }
        )

        if not query['Item']:
            return None

        return query['Item']

    except Exception as e:
        print(f"ERROR: {e}")
        return None


def queryDeleteDownvoteForPost(postId, userId):
    """
    Function to delete a downvote with the given postId and userId
    """
    try:
        downvotes_table.delete_item(Key={
            'postId': postId,
            'userId': userId
        })
        return True
    except Exception:
        return False


def queryGetDownvotesCountForPost(postId):
    """
    Function to retrieve the total count of downvotes for a given post
    """
    try:
        query = downvotes_table.scan(
            FilterExpression=Attr('postId').eq(postId),
            Select="COUNT"
        )

        if query is None or 'Count' not in query:
            return None

        return query['Count']

    except Exception as e:
        print(f"ERROR: {e}")
        return None
