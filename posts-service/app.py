from flask import Flask, request, make_response
from flask_cors import CORS
from middleware.tokens import authTokenRequired
from utils.requests import (
    getGroupNameFromRequestBody,
    getPostFromRequestBody,
    getResponseFromRequestBody
)
from db.posts import (
    queryCreateNewPost,
    queryGetPostsForGroupPaginated,
    queryGetPostById,
    queryUpdatePost,
    queryDeletePostWithId,
    queryCreateNewResponse,
    queryGetResponseById,
    queryGetResponsesPaginated,
    queryDeleteResponseWithId,
    queryUpdateResponse,
    queryAllPostsForGroupsPaginated
)
from db.votes import (
    queryAddUpvoteToPost,
    queryDeleteUpvoteForPost,
    queryGetUpvotesCountForPost,
    queryGetUpvoteForPost,
    queryAddDownvoteToPost,
    queryDeleteDownvoteForPost,
    queryGetDownvotesCountForPost,
    queryGetDownvoteForPost
)
import requests
import simplejson as json
import os

# load environment variables
groups_service_url = os.environ.get('GROUPS_SERVICE_URL')

# Create a new Flask app
app = Flask(__name__)

# Set up CORS
CORS(app, resources={r"/*": {"origins": "*"}})


##########################################################
# ENDPOINT: /api/v1/posts/feed?limit=<limit>&lastReceivedId=<lastReceivedId>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/posts/feed', methods=['GET'])
@authTokenRequired
def handleUserFeedRequest(context={}):
    # retrieve the groups that a user is a part of
    # check group exists and user is a member of the group
    url = f"{groups_service_url}/user"
    token = context.get("token")
    response = requests.get(url, params={'token': token})
    if response.status_code != 200:
        return {'error': 'group with given id does not exist'}, 400

    data = json.loads(response.text)
    if 'groups' not in data:
        return {'error': 'could not retrieve user\'s groups'}, 500

    groups = data['groups']
    if len(groups) == 0:
        return json.dumps([]), 200

    groups = [group['groupName'] for group in groups]
    feed = queryAllPostsForGroupsPaginated(groups)
    if feed is None:
        return {'error': 'could not create users feed'}, 500

    return json.dumps(feed), 200


##########################################################
# ENDPOINT: /api/v1/posts?limit=<limit>&lastReceivedId=<lastReceivedId>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/posts', methods=['GET'])
@authTokenRequired
def handleGetPostsRequest(context={}):
    # Get query parameters used for paginated requests
    lastReceivedId = request.args.get('lastReceivedId', None)
    limit = request.args.get('limit', 20)

    groupName = request.args.get("group", None)
    if groupName is None:
        return {'error': 'group name not found in query paramaters'}, 400

    # check group exists
    url = f"{groups_service_url}/{groupName}"
    token = context.get("token")
    response = requests.get(url, params={'token': token})
    if response.status_code != 200:
        return {'error': 'group with given id does not exist'}, 400

    # Create a new post in the database
    posts = queryGetPostsForGroupPaginated(groupName, limit, lastReceivedId)
    if posts is None:
        return {'error': 'could not retrieve posts'}, 500

    return json.dumps(posts), 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/posts/<postId>', methods=['GET'])
@authTokenRequired
def handleGetPostRequest(postId, context={}):
    # retrieve the post with the given id
    post = queryGetPostById(postId)
    print(f"POST: {post}")
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    # check user is a member of the group the post belongs to
    groupName = post['groupName']
    url = f"{groups_service_url}/{groupName}"
    token = context.get("token")
    response = requests.get(url, params={'token': token})
    if response.status_code != 200:
        return {'error': 'group with given name does not exist'}, 400

    return json.dumps(post), 200


##########################################################
# ENDPOINT: /api/v1/posts
# EXCEPTED METHODS: POST
#
#
##########################################################
@app.route('/api/v1/posts', methods=['POST'])
@authTokenRequired
def handleCreatePostRequest(context={}):
    # get the id of the user making the request
    userId = context.get('userId')

    # get the post details from the request body
    post = getPostFromRequestBody(request)
    if post is None:
        return {'error': 'post not found in request body'}, 400

    # check group exists and user is a member of the group
    groupName = post['groupName']
    url = f"{groups_service_url}/{groupName}"
    token = context.get("token")
    response = requests.get(url, params={'token': token})
    if response.status_code != 200:
        return {'error': 'group with given id does not exist'}, 400

    # Create the post in the database
    post = queryCreateNewPost(userId, post)
    if post is None:
        return {'error': 'unable to create new post'}, 500

    return json.dumps(post), 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>
# EXCEPTED METHODS: PUT
#
#
##########################################################
@app.route('/api/v1/posts/<postId>', methods=['PUT'])
@authTokenRequired
def handleUpdatePostRequest(postId, context={}):
    userId = context.get('userId')

    # get the post details from the request body
    updatedPost = getPostFromRequestBody(request)
    if updatedPost is None:
        return {'error': 'post not found in request body'}

    # retrieve the original post
    originalPost = queryGetPostById(postId)
    if originalPost is None:
        return {'error': 'could not find post with the given id'}, 400

    # check user is a member of the group the post belongs to
    groupName = originalPost['groupName']
    url = f"{groups_service_url}/{groupName}"
    token = context.get("token")
    response = requests.get(url, params={'token': token})
    if response.status_code != 200:
        return {'error': 'group with given id does not exist'}, 400

    # check that the original post was created by the current user
    if userId != originalPost['postedBy']:
        return {'error': 'cannot update a post you did not create'}, 403

    # update the post in the database
    updatedPost['createdAt'] = originalPost['createdAt']
    post = queryUpdatePost(userId, postId, updatedPost)
    if post is None:
        return {'error': 'unable to update the post'}, 200

    return json.dumps(post), 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>
# EXCEPTED METHODS: DELETE
#
#
##########################################################
@app.route('/api/v1/posts/<postId>', methods=['DELETE'])
@authTokenRequired
def handleDeletePostRequest(postId, context={}):
    userId = context.get('userId')

    # check that the post exists
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    # check user is a member of the group the post belongs to
    groupName = post['groupName']
    url = f"{groups_service_url}/{groupName}"
    token = context.get("token")
    response = requests.get(url, params={'token': token})
    if response.status_code != 200:
        return {'error': 'group with given id does not exist'}, 400

    # check that the original post was created by the current user
    if userId != post['postedBy']:
        return {'error': 'cannot delete a post you did not create'}, 403

    # delete the post from the database
    wasDeleted = queryDeletePostWithId(postId)
    if not wasDeleted:
        return {'error': 'could not delete post'}, 500

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>/responses
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/posts/<postId>/responses', methods=['GET'])
@authTokenRequired
def handleGetPostResponsesRequest(postId, context={}):
    # Get query parameters used for paginated requests
    lastReceivedId = request.args.get('lastReceivedId') or None
    limit = request.args.get('limit') or 20

    # retrieve the post with the given id
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    # check user is a member of the group the post belongs to
    groupName = post['groupName']
    url = f"{groups_service_url}/{groupName}"
    token = context.get("token")
    response = requests.get(url, params={'token': token})
    if response.status_code != 200:
        return {'error': 'group with given id does not exist'}, 400

    # fetch responses from the database
    responses = queryGetResponsesPaginated(postId, limit, lastReceivedId)
    if responses is None:
        return {'error': 'unable to retrieve responses for this post'}, 500

    return json.dumps(responses), 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>/responses/<responseId>
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/posts/<postId>/responses/<responseId>', methods=['GET'])
@authTokenRequired
def handleGetPostResponseRequest(postId, responseId, context={}):
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    # check user is a member of the group the post belongs to
    groupName = post['groupName']
    url = f"{groups_service_url}/{groupName}"
    token = context.get("token")
    response = requests.get(url, params={'token': token})
    if response.status_code != 200:
        return {'error': 'group with given id does not exist'}, 400

    # get the response with the given id from the database
    response = queryGetResponseById(responseId)
    if response is None:
        return {'error': 'could not find response with the given id'}, 400

    return json.dumps(response), 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>/responses
# EXCEPTED METHODS: POST
#
#
##########################################################
@app.route('/api/v1/posts/<postId>/responses', methods=['POST'])
@authTokenRequired
def handleCreatePostResponseRequest(postId, context={}):
    userId = context.get('userId')

    # get the response from the request body
    postResponse = getResponseFromRequestBody(request)
    if postResponse is None:
        return {'error': 'no response provided in the request body'}, 200

    # get the post with the given id from the database
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    # check user is a member of the group the post belongs to
    groupName = post['groupName']
    url = f"{groups_service_url}/{groupName}"
    token = context.get("token")
    response = requests.get(url, params={'token': token})
    if response.status_code != 200:
        return {'error': 'group with given id does not exist'}, 400

    # Create a new response in the database
    response = queryCreateNewResponse(userId, postId, postResponse)
    if response is None:
        return {'error': 'unable to create response'}, 500

    return json.dumps(response), 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>/responses/<responseId>
# EXCEPTED METHODS: PUT
#
#
##########################################################
@app.route('/api/v1/posts/<postId>/responses/<responseId>', methods=['PUT'])
@authTokenRequired
def handleUpdatePostResponseRequest(postId, responseId, context={}):
    userId = context.get('userId')

    # get response from the request body
    updatedResponse = getResponseFromRequestBody(request)
    if updatedResponse is None:
        return {'error': 'no response provided in the request body'}, 200

    # get the post with the given id from the database
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    # check user is a member of the group the post belongs to
    groupName = post['groupName']
    url = f"{groups_service_url}/{groupName}"
    token = context.get("token")
    response = requests.get(url, params={'token': token})
    if response.status_code != 200:
        return {'error': 'group with given id does not exist'}, 400

    # get the original response from the database
    originalResponse = queryGetResponseById(responseId)
    if not originalResponse:
        return {'error': 'could not find response with the given id'}, 400

    # update the response in the database
    response = queryUpdateResponse(userId, postId, responseId, updatedResponse)
    if response is None:
        return {'error', 'could not update response'}, 500

    return json.dumps(response), 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>/responses/<responseId>
# EXCEPTED METHODS: DELETE
#
#
##########################################################
@app.route('/api/v1/posts/<postId>/responses/<responseId>', methods=['DELETE'])
@authTokenRequired
def handleDeletePostResponseRequest(postId, responseId, context={}):
    userId = context.get('userId')

    # get the post with the given id from the database
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    # check user is a member of the group the post belongs to
    groupName = post['groupName']
    url = f"{groups_service_url}/{groupName}"
    token = context.get("token")
    response = requests.get(url, params={'token': token})
    if response.status_code != 200:
        return {'error': 'group with given id does not exist'}, 400

    # Get the response from the database
    response = queryGetResponseById(responseId)
    if response is None:
        return {'error': 'could not find response with the given id'}, 400

    # ensure the response was created by the current user
    if userId != response['postedBy']:
        return {'error': 'cannot delete a response that is not your own'}, 403

    # delete the response from the database
    wasDeleted = queryDeleteResponseWithId(responseId)
    if not wasDeleted:
        return {'error': 'unable to delete response with the given id'}, 500

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>/upvotes
# EXCEPTED METHODS: POST
#
#
##########################################################
@app.route('/api/v1/posts/<postId>/upvotes', methods=['POST'])
@authTokenRequired
def handleAddUpvoteRequest(postId, context={}):
    userId = context.get('userId')

    # get the post with the given id from the database
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    # create an entry for the upvotes in the database
    upvote = queryAddUpvoteToPost(postId, userId)
    if upvote is None:
        return {'error': 'unable to add upvote for the post'}, 500

    return {'upvote': upvote}, 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>/upvotes
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/posts/<postId>/upvotes/count', methods=['GET'])
@authTokenRequired
def handleGetUpvotesCountRequest(postId, context={}):
    # get the post with the given id from the database
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    count = queryGetUpvotesCountForPost(postId)
    if count is None:
        return {'error': 'could not retrieve upvote count for this post'}, 500

    return {'upvotes': count}, 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>/upvotes
# EXCEPTED METHODS: DELETE
#
#
##########################################################
@app.route('/api/v1/posts/<postId>/upvotes', methods=['DELETE'])
@authTokenRequired
def handleDeleteUpvoteRequest(postId, context={}):
    userId = context.get('userId')

    # get the post with the given id from the database
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    upvote = queryGetUpvoteForPost(postId, userId)
    if upvote is None:
        return {'error': 'user did not upvote this post before'}, 400

    wasDeleted = queryDeleteUpvoteForPost(postId, userId)
    if not wasDeleted:
        return {'error': 'unable to delete upvote for post'}, 500

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>/downvotes
# EXCEPTED METHODS: POST
#
#
##########################################################
@app.route('/api/v1/posts/<postId>/downvotes', methods=['POST'])
@authTokenRequired
def handleAddDownvoteRequest(postId, context={}):
    userId = context.get('userId')

    # get the post with the given id from the database
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    # create an entry for the upvotes in the database
    downvote = queryAddDownvoteToPost(postId, userId)
    if downvote is None:
        return {'error': 'unable to add downvote for the post'}, 500

    return {'downvote': downvote}, 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>/downvotes
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route('/api/v1/posts/<postId>/downvotes/count', methods=['GET'])
@authTokenRequired
def handleGetDownvotesCountRequest(postId, context={}):
    # get the post with the given id from the database
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    count = queryGetDownvotesCountForPost(postId)
    if count is None:
        return {'error': 'could not retrieve downvote count for post'}, 500

    return {'downvotes': count}, 200


##########################################################
# ENDPOINT: /api/v1/posts/<postId>/downvotes
# EXCEPTED METHODS: DELETE
#
#
##########################################################
@app.route('/api/v1/posts/<postId>/downvotes', methods=['DELETE'])
@authTokenRequired
def handleDeleteDownvoteRequest(postId, context={}):
    userId = context.get('userId')

    # get the post with the given id from the database
    post = queryGetPostById(postId)
    if post is None:
        return {'error': 'could not find post with the given id'}, 400

    downvote = queryGetDownvoteForPost(postId, userId)
    if downvote is None:
        return {'error': 'user did not downvote this post before'}, 400

    wasDeleted = queryDeleteDownvoteForPost(postId, userId)
    if not wasDeleted:
        return {'error': 'unable to delete downvote for post'}, 500

    return {}, 200


##########################################################
# ENDPOINT: /api/v1/posts/health-check
# EXCEPTED METHODS: GET, PUT, or POST
#
#
##########################################################
@app.route("/api/v1/posts/health-check", methods=["GET", "PUT", "POST"])
def handleHealthCheckRequest():
    return {}, 200


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
