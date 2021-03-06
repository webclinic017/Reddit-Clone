from uuid import uuid4
import boto3
import time
from boto3.dynamodb.conditions import Attr
import os


posts_table_name = os.environ.get('POSTS_DYNAMODB_TABLE_NAME')
responses_table_name = os.environ.get('RESPONSES_DYNAMODB_TABLE_NAME')

dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION'))
posts_table = dynamodb.Table(posts_table_name)
responses_table = dynamodb.Table(responses_table_name)


def queryCreateNewPost(userId, post):
    """
    Function to create a new post in the dynamoDB table
    """
    try:
        newPostId = uuid4().hex
        createdAt = int(time.time())
        posts_table.put_item(Item={
            'postId': newPostId,
            'groupName': post['groupName'],
            'postedBy': userId,
            'title': post['title'],
            'post': post['post'],
            'createdAt': createdAt
        })

        post['postId'] = newPostId
        post['postedBy'] = userId
        return post
    except Exception:
        return None


def queryGetPostsForGroupPaginated(groupName, limit, lastReceivedId):
    """
    Function to retrieve all posts for a given group from the database.
    The function implements pagination using limit and lastReceivedId
    arguments
    """
    try:
        query = None

        if lastReceivedId:
            query = posts_table.scan(
                Limit=int(limit),
                FilterExpression=Attr('groupName').eq(groupName),
                ExclusiveStartKey={'postId': lastReceivedId}
            )
        else:
            query = posts_table.scan(
                FilterExpression=Attr('groupName').eq(groupName),
                Limit=int(limit),
            )

        if not query or 'Items' not in query:
            return None

        return query['Items']

    except Exception:
        return None


def queryGetPostById(postId):
    """
    Function to retrieve the post with the given id from the database
    """
    try:
        query = posts_table.get_item(
            Key={
                "postId": postId
            }
        )

        if not query['Item']:
            return None

        return query['Item']

    except Exception:
        return None


def queryUpdatePost(userId, postId, post):
    """
    Function to update a post in the dynamoDB table
    """
    try:
        posts_table.put_item(Item={
            'postId': postId,
            'groupName': post['groupName'],
            'postedBy': userId,
            'title': post['title'],
            'post': post['post'],
            'createdAt': post['createdAt']
        })

        post['postId'] = postId
        post['userId'] = userId
        return post
    except Exception:
        return None


def queryDeletePostWithId(postId):
    """
    Function to delete a post with the given id from the dynamoDB table
    """
    try:
        posts_table.delete_item(Key={'postId': postId})
        return True
    except Exception:
        return False


def queryCreateNewResponse(userId, postId, response):
    """
    Function to create a new response in the dynamoDB table
    """
    try:
        newResponseId = uuid4().hex
        createdAt = int(time.time())
        newResponse = {
            'responseId': newResponseId,
            'postId': postId,
            'postedBy': userId,
            'response': response,
            'createdAt': createdAt
        }

        responses_table.put_item(Item=newResponse)

        return newResponse
    except Exception as e:
        print(e)
        return None


def queryGetResponseById(responseId):
    """
    Function to retrieve a response with the given id from the dynamoDB table
    """
    try:
        query = responses_table.get_item(
            Key={
                "responseId": responseId
            }
        )

        if not query['Item']:
            return None

        return query['Item']

    except Exception:
        return None


def queryGetResponsesPaginated(postId, limit, lastReceivedId):
    """
    Function to retrieve all responses for a given post from the database.
    The function implements pagination using limit and lastReceivedId
    arguments
    """
    try:
        query = None

        if lastReceivedId:
            query = responses_table.scan(
                Limit=int(limit),
                FilterExpression=Attr('postId').eq(postId),
                ExclusiveStartKey={'postId': lastReceivedId}
            )
        else:
            query = responses_table.scan(
                FilterExpression=Attr('postId').eq(postId),
                Limit=int(limit),
            )

        if not query or 'Items' not in query:
            return None

        return query['Items']

    except Exception:
        return None


def queryDeleteResponseWithId(responseId):
    """
    Function to delete the response with the given id from the dynamoDB table
    """
    try:
        responses_table.delete_item(Key={'responseId': responseId})
        return True
    except Exception:
        return False


def queryUpdateResponse(userId, postId, responseId, response):
    """
    Function to update the response with the given id
    TODO: Need to keep createAt time
    """
    try:
        updatedResponse = {
            'responseId': responseId,
            'postId': postId,
            'postedBy': userId,
            'reponse': response
        }

        responses_table.put_item(Item=updatedResponse)

        return updatedResponse
    except Exception as e:
        print(e)
        return None


def queryAllPostsForGroupsPaginated(groupNames, limit=20, lastReceivedId=None):
    try:
        query = None

        if lastReceivedId:
            query = posts_table.scan(
                Limit=int(limit),
                FilterExpression=Attr('groupName').is_in(groupNames),
                ExclusiveStartKey={'postId': lastReceivedId}
            )
        else:
            query = posts_table.scan(
                FilterExpression=Attr('groupName').is_in(groupNames),
                Limit=int(limit),
            )

        if not query or 'Items' not in query:
            return None

        return query['Items']

    except Exception as err:
        print(f"ERROR: {err}")
        return None
