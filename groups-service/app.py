from flask import Flask, request, make_response
from flask_cors import CORS
from middleware.tokens import authTokenRequired
from dotenv import dotenv_values
from utils.requests import getCreateGroupFieldsFromRequest
from db.queries import (
    queryCreateNewGroup,
    queryGetGroupById,
    queryGetGroupsPaginated,
    queryDeleteGroupWithId,
    queryUpdateGroup,
    queryCreateNewGroupMembership,
    queryLookupMembership,
    queryDeleteMembership,
    queryGetGroupMembersPaginated,
    queryGetUsersGroups
)


# Create a new Flask app
app = Flask(__name__)

# Set up CORS
CORS(app, resources={r"/*": {"origins": "*"}})


##########################################################
# ENDPOINT: /api/v1/groups?lastReceivedId=<lastReceivedId>&limit=<limit>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/groups', methods=['GET'])
@authTokenRequired
def handleGetGroupsRequest(context={}):
    # Get query parameters used for paginated requests
    lastReceivedId = request.args.get('lastReceivedId') or None
    limit = request.args.get('limit') or 20

    # query db for list of groups
    groups = queryGetGroupsPaginated(lastReceivedId, limit)
    if groups is None:
        return {'error': 'Unable to query groups in database'}, 500

    return {'groups': groups}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<group_id>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/groups/<group_id>', methods=['GET'])
@authTokenRequired
def handleGetGroupRequest(group_id, context={}):
    # retrive the group with the given id
    group = queryGetGroupById(group_id)
    if group is None:
        return {'error': 'could not find group with matching id'}, 400

    return {'group': group}, 200


##########################################################
# ENDPOINT: /api/v1/groups
# EXCEPTED METHODS: POST
#
#
##########################################################
@app.route('/api/v1/groups', methods=['POST'])
@authTokenRequired
def handleCreateGroupRequest(context={}):
    userId = context.get('userId', None)

    group = getCreateGroupFieldsFromRequest(request)
    if group is None:
        return {'error': 'request body does not contain a valid group'}, 400

    groupId = queryCreateNewGroup(userId, group['name'], group['description'])
    if groupId is None:
        return {'error': 'unable to create new group'}, 500

    return {'groupId': groupId}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<group_id>
# EXCEPTED METHODS: PUT
#
#
##########################################################
@app.route('/api/v1/groups/<group_id>', methods=['PUT'])
@authTokenRequired
def handleUpdateGroupRequest(group_id, context={}):
    userId = context.get('userId', None)

    # check that request body contains a valid group
    updatedGroup = getCreateGroupFieldsFromRequest(request)
    if updatedGroup is None:
        return {'error': 'request body does not contain a valid group'}, 400

    # Retrieve the existing group
    group = queryGetGroupById(group_id)
    if not group:
        return {'error': 'no group found with matching id'}, 400

    # check that the user is the one who created the group
    createdBy = group['created_by']
    if createdBy != userId:
        return {'error': 'cannot update a group you did not create'}, 403

    # Update the group in the database
    wasUpdated = queryUpdateGroup(
        group_id, updatedGroup['name'], updatedGroup['description'])
    if not wasUpdated:
        return {'error': 'unable to update group'}, 500

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<group_id>
# EXCEPTED METHODS: DELETE
#
#
##########################################################
@app.route('/api/v1/groups/<group_id>', methods=['DELETE'])
@authTokenRequired
def handleDeleteGroupsRequest(group_id, context={}):
    userId = context.get('userId')

    group = queryGetGroupById(group_id)
    if not group:
        return {'error': 'no group found with matching id'}, 400

    createdBy = group['created_by']
    if createdBy != userId:
        return {'error': 'cannot delete a group you did not create'}, 403

    wasDeleted = queryDeleteGroupWithId(group_id)
    if not wasDeleted:
        return {'error': 'could not delete group'}, 500

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<group_id>/members?limit=<limit>&lastReceivedId=<lastReceivedId>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/groups/<group_id>/members', methods=['GET'])
@authTokenRequired
def handleGetGroupMembersRequest(group_id, context={}):
    # Get query parameters used for paginated requests
    lastReceivedId = request.args.get('lastReceivedId') or None
    limit = request.args.get('limit') or 20

    group = queryGetGroupById(group_id)
    if not group:
        return {'error': 'invalid group id'}, 400

    members = queryGetGroupMembersPaginated(group_id, lastReceivedId, limit)
    if members is None:
        return {'error': 'unable to retrieve group members'}, 500

    return {'members': members}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<group_id>/members/<user_id>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/groups/<group_id>/members/<user_id>', methods=['GET'])
@authTokenRequired
def handleGetGroupMemberRequest(group_id, user_id, context={}):
    membership = queryLookupMembership(group_id, user_id)
    if not membership:
        return {'error': 'membership does not exist'}, 400

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<group_id>/members
# EXCEPTED METHODS: POST
#
#
##########################################################
@app.route('/api/v1/groups/<group_id>/members', methods=['POST'])
@authTokenRequired
def handleAddGroupMemberRequest(group_id, context={}):
    userId = context.get('userId')

    membership = queryLookupMembership(group_id, userId)
    if membership:
        return {'error': 'membership already exists'}, 400

    wasCreated = queryCreateNewGroupMembership(group_id, userId)
    if not wasCreated:
        return {'error': 'unable to create new group membership'}, 500

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<group_id>/members
# EXCEPTED METHODS: DELETE
#
#
##########################################################
@app.route('/api/v1/groups/<group_id>/members', methods=['DELETE'])
@authTokenRequired
def handleDeleteGroupMemberRequest(group_id, context={}):
    userId = context.get('userId')

    membership = queryLookupMembership(group_id, userId)
    if not membership:
        return {'error': 'membership does not exist'}, 400

    wasDeleted = queryDeleteMembership(group_id, userId)
    if not wasDeleted:
        return {'error': 'unable to delete the membership'}, 500

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/groups/user
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/groups/user', methods=['GET'])
@authTokenRequired
def handleGetUsersGroupsRequest(context={}):
    userId = context.get('userId')

    groups = queryGetUsersGroups(userId)
    if groups is None:
        return {'error': 'could not retrieved user\'s groups'}, 500

    return {'groups': groups}, 200


##########################################################
# ENDPOINT: /api/v1/groups/health-check
# EXCEPTED METHODS: GET, PUT, or POST
#
#
##########################################################
@app.route("/api/v1/groups/health-check", methods=["GET", "PUT", "POST"])
def handleHealthCheckRequest():
    return {}, 200


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
