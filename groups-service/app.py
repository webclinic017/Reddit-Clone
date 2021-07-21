from flask import Flask, request, make_response
from flask_cors import CORS
from middleware.tokens import authTokenRequired
from utils.requests import getCreateGroupFieldsFromRequest
from db.queries import (
    queryCreateNewGroup,
    queryGetGroupByName,
    queryGetGroupsPaginated,
    queryDeleteGroupWithName,
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
# ENDPOINT: /api/v1/groups?lastReceivedName=<lastReceivedName>&limit=<limit>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/groups', methods=['GET'])
@authTokenRequired
def handleGetGroupsRequest(context={}):
    # Get query parameters used for paginated requests
    lastReceivedName = request.args.get('lastReceivedName') or None
    limit = request.args.get('limit') or 20

    # query db for list of groups
    groups = queryGetGroupsPaginated(lastReceivedName, limit)
    if groups is None:
        return {'error': 'Unable to query groups in database'}, 500

    return {'groups': groups}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<groupName>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/groups/<groupName>', methods=['GET'])
@authTokenRequired
def handleGetGroupRequest(groupName, context={}):
    # retrive the group with the given id
    group = queryGetGroupByName(groupName)
    if group is None:
        return {'error': 'could not find group with given name'}, 400

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

    existingGroup = queryGetGroupByName(group['name'])
    if existingGroup:
        return {'error': 'group with given name already exists'}, 400

    groupName = queryCreateNewGroup(
        userId, group['name'], group['description'])
    if groupName is None:
        return {'error': 'unable to create new group'}, 500

    return {'groupName': groupName}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<group_id>
# EXCEPTED METHODS: PUT
#
#
##########################################################
@app.route('/api/v1/groups/<groupName>', methods=['PUT'])
@authTokenRequired
def handleUpdateGroupRequest(groupName, context={}):
    userId = context.get('userId', None)

    # check that request body contains a valid group
    updatedGroup = getCreateGroupFieldsFromRequest(request)
    if updatedGroup is None:
        return {'error': 'request body does not contain a valid group'}, 400

    # Retrieve the existing group
    group = queryGetGroupByName(groupName)
    if not group:
        return {'error': 'no group found with matching id'}, 400

    # check that the user is the one who created the group
    createdBy = group['created_by']
    if createdBy != userId:
        return {'error': 'cannot update a group you did not create'}, 403

    # Update the group in the database
    wasUpdated = queryUpdateGroup(
        groupName, updatedGroup['description'])
    if not wasUpdated:
        return {'error': 'unable to update group'}, 500

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<groupName>
# EXCEPTED METHODS: DELETE
#
#
##########################################################
@app.route('/api/v1/groups/<groupName>', methods=['DELETE'])
@authTokenRequired
def handleDeleteGroupsRequest(groupName, context={}):
    userId = context.get('userId')

    group = queryGetGroupByName(groupName)
    if not group:
        return {'error': 'no group found with matching id'}, 400

    createdBy = group['created_by']
    if createdBy != userId:
        return {'error': 'cannot delete a group you did not create'}, 403

    wasDeleted = queryDeleteGroupWithName(groupName)
    if not wasDeleted:
        return {'error': 'could not delete group'}, 500

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<groupName>/members?limit=<limit>&lastReceivedId=<lastReceivedId>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/groups/<groupName>/members', methods=['GET'])
@authTokenRequired
def handleGetGroupMembersRequest(groupName, context={}):
    # Get query parameters used for paginated requests
    lastReceivedId = request.args.get('lastReceivedId') or None
    limit = request.args.get('limit') or 20

    group = queryGetGroupByName(groupName)
    if not group:
        return {'error': 'invalid group id'}, 400

    members = queryGetGroupMembersPaginated(groupName, lastReceivedId, limit)
    if members is None:
        return {'error': 'unable to retrieve group members'}, 500

    return {'members': members}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<group_id>/members/<user_id>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/groups/<groupName>/members/<user_id>', methods=['GET'])
@authTokenRequired
def handleGetGroupMemberRequest(groupName, user_id, context={}):
    membership = queryLookupMembership(groupName, user_id)
    if not membership:
        return {'error': 'membership does not exist'}, 400

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<group_id>/members
# EXCEPTED METHODS: POST
#
#
##########################################################
@app.route('/api/v1/groups/<groupName>/members', methods=['POST'])
@authTokenRequired
def handleAddGroupMemberRequest(groupName, context={}):
    userId = context.get('userId')

    membership = queryLookupMembership(groupName, userId)
    if membership:
        return {'error': 'membership already exists'}, 400

    wasCreated = queryCreateNewGroupMembership(groupName, userId)
    if not wasCreated:
        return {'error': 'unable to create new group membership'}, 500

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/groups/<groupName>/members
# EXCEPTED METHODS: DELETE
#
#
##########################################################
@app.route('/api/v1/groups/<groupName>/members', methods=['DELETE'])
@authTokenRequired
def handleDeleteGroupMemberRequest(groupName, context={}):
    userId = context.get('userId')

    membership = queryLookupMembership(groupName, userId)
    if not membership:
        return {'error': 'membership does not exist'}, 400

    wasDeleted = queryDeleteMembership(groupName, userId)
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
    app.run(threaded=True, host='0.0.0.0', port=5001)
