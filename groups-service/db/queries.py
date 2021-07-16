from uuid import uuid4
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os


groups_table_name = os.environ.get('GROUPS_DYNAMODB_TABLE_NAME')
members_table_name = os.environ.get('MEMBERS_DYNAMODB_TABLE_NAME')

dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION'))
groups_table = dynamodb.Table(groups_table_name)
members_table = dynamodb.Table(members_table_name)


def queryCreateNewGroup(userId, group_name, group_description):
    """
    Helper function to create a new group
    """
    try:
        newGroupId = uuid4().hex
        groups_table.put_item(Item={
            'groupId': newGroupId,
            'name': group_name,
            'description': group_description,
            'created_by': userId,
        })

        return newGroupId
    except Exception:
        return None


def queryGetGroupById(groupId):
    """
    Helper function to retrieve a group from the dynamoDB groups table
    based on its Id
    """
    try:
        query = groups_table.get_item(
            Key={
                "groupId": groupId
            }
        )

        if not query['Item']:
            return None

        return query['Item']

    except Exception:
        return None


def queryGetGroupsPaginated(lastReceivedGroupId, limit):
    """
    helper function to query a list of groups from the dynamoDB groups
    table. Supports pagination by providing a limit of resources to return
    and the lastReceivedGroupId for offset parameter.
    """
    try:
        query = None

        if lastReceivedGroupId:
            query = groups_table.scan(
                Limit=int(limit),
                ExclusiveStartKey={'groupId': lastReceivedGroupId}
            )
        else:
            query = groups_table.scan(
                Limit=int(limit),
            )

        if not query or 'Items' not in query:
            return None

        return query['Items']

    except Exception:
        return None


def queryUpdateGroup(groupId, name, description):
    """
    helper function to query the dynamoDB groups table to update a
    groups name and description
    """
    try:
        group = queryGetGroupById(groupId)
        if group is None:
            return False

        groups_table.put_item(Item={
            'groupId': group['groupId'],
            'name': name,
            'description': description,
            'created_by': group['created_by'],
        })

        return True

    except Exception:
        return False


def queryDeleteGroupWithId(groupId):
    """
    helper function to query the dynamoDB groups table to delete a group
    with the given groupId
    """
    try:
        groups_table.delete_item(Key={'groupId': groupId})
        return True
    except Exception:
        return False


def queryCreateNewGroupMembership(groupId, userId):
    """
    helper function to query the dynamoDB members table to create a new
    group membership entry
    """
    try:
        members_table.put_item(
            Item={
                'groupId': groupId,
                'userId': userId
            }
        )

        return True

    except Exception:
        return False


def queryLookupMembership(groupId, userId):
    """
    helper function to query the dynamoDB members table to lookup is
    a user with the given userId is a member of the group with the given
    groupId
    """
    try:
        query = members_table.get_item(
            Key={
                'groupId': groupId,
                'userId': userId
            }
        )

        if not query['Item']:
            return None

        return query['Item']

    except Exception:
        return None


def queryDeleteMembership(groupId, userId):
    """
    helper function to query the dynamoDB members table to delete the entry
    for membership with the given groupId and userId
    """
    try:
        members_table.delete_item(
            Key={
                'groupId': groupId,
                'userId': userId
            }
        )

        return True

    except Exception:
        return False


def queryGetGroupMembersPaginated(groupId, lastReceivedMemberId, limit):
    """
    helper function to query a list of group members from the dynamoDB members
    table. Supports pagination by providing a limit of resources to return
    and the lastReceivedMemberId for offset parameter.
    """
    try:
        query = None

        if lastReceivedMemberId:
            query = members_table.scan(
                FilterExpression=Attr('groupId').eq(groupId),
                Limit=int(limit),
                ExclusiveStartKey={
                    'groupId': groupId,
                    'userId': lastReceivedMemberId
                }
            )
        else:
            query = members_table.query(
                KeyConditionExpression=Key('groupId').eq(groupId),
                Limit=int(limit),
            )

        if query is None or 'Items' not in query:
            return None

        return query['Items']

    except Exception:
        return None


def queryGetUsersGroups(userId):
    """
    helper function to query the dynamoDB members table to get a list
    of all the groups the user with the given userId is a member of
    """
    try:
        query = members_table.scan(
            ProjectionExpression='groupId',
            FilterExpression=Attr('userId').eq(userId),
        )

        if query is None or 'Items' not in query:
            return None

        return query["Items"]

    except Exception:
        return None
