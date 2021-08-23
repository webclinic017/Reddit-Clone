from flask import Flask, request, make_response
from flask_cors import CORS
from utils.tokens import TokenManager
from utils.requests import (
    getLoginCredentialsFromRequest,
    getRegisterCredentialsFromRequest,
    isRequestFromSavedTokenHolder
)
from utils.hash import checkPasswordMatchesHash, hash
from db.queries import (
    queryUserByEmail,
    queryCreateNewUser,
    queryCreateNewToken,
    queryDeleteToken,
    queryTokenByUserId,
    queryUsernameForUserId
)
from middleware.tokens import authTokenRequired, validateTokenSender
from middleware.requests import addRequestSenderDataToContext
import os
import json

# Create a new Flask app
app = Flask(__name__)

# get allowed origins as environment variable
allowed_origins = os.environ.get("ALLOWED_ORIGINS") or "*"

# Set up CORS
CORS(app, resources={r"/*": {"origins": allowed_origins}})

# create manager for JWTs
tokenManager = TokenManager()


@app.route("/api/v1/auth/login", methods=["POST"])
@addRequestSenderDataToContext
def handleUserLogin(context={}):
    """
    ENDPOINT: /api/v1/auth/login
    EXCEPTED METHODS: POST
    """

    ipAddr = context.get('ipAddr')

    # check that email and password were provided in the request body
    credentials = getLoginCredentialsFromRequest(request)
    if not credentials:
        return {"error": "email and password not provided"}, 400

    # check that a user with the given email exists
    user = queryUserByEmail(credentials['email'])
    if not user:
        return {"error": "invalid credentials"}, 400

    # check that the provided password matches stored password
    providedPassword = credentials['password']
    password = user['password']
    if not checkPasswordMatchesHash(providedPassword, password):
        return {"error": "invalid credentials"}, 400

    # try to retrieve an existing authentication token
    savedToken = queryTokenByUserId(user.get('userId'), ipAddr)

    # if a token already exists for the current user
    if savedToken:
        # if saved token identifies this user and device
        # delete the token and create a new one
        if isRequestFromSavedTokenHolder(request, savedToken):
            queryDeleteToken(user.get('userId'), ipAddr)
        else:
            return {'error': 'invalid credential'}, 400

    # Create a JWT to identify the user in new requests
    userId = user['userId']
    token = tokenManager.create(userId, 1500)
    if not token:
        return {'error': 'unable to create auth token'}, 500

    # save the users tokens
    userAgent = context.get('userAgent')
    tokenSaved = queryCreateNewToken(userId, ipAddr, userAgent, token)
    if not tokenSaved:
        return {'error': 'unable to save auth token'}, 500

    # create response to the user
    res = make_response()

    # send token as an http only cookie
    res.set_cookie('auth_token', token, httponly=True)

    # remove password field before sending user data in response
    del user['password']

    # also send token in response body
    res.set_data(json.dumps({"user": user, "token": token}))
    return res, 200


@app.route("/api/v1/auth/register", methods=["POST"])
@addRequestSenderDataToContext
def handleUserRegister(context={}):
    """
    ENDPOINT: /api/v1/auth/register
    EXCEPTED METHODS: POST
    """

    # check that username, email, and password were provided in the request
    credentials = getRegisterCredentialsFromRequest(request)
    if not credentials:
        return {"error": "username, email, and password not provided"}, 400

    # check that a user with the given email does not exist
    user = queryUserByEmail(credentials['email'])
    if user:
        return {"error": "email already in use"}, 400

    # Hash user password and create new user in the database
    hashedPassword = hash(credentials['password'])
    newUser = queryCreateNewUser(
        credentials['username'], credentials['email'], hashedPassword)
    if not newUser:
        return {'error': 'unable to create a new user account'}, 500

    # Create a JWT to identify the user in new requests
    token = tokenManager.create(newUser['userId'], 1500)
    if not token:
        return {'error': 'unable to create auth token'}, 500

    # save the users tokens
    ipAddr = context.get('ipAddr')
    userAgent = context.get('userAgent')
    tokenSaved = queryCreateNewToken(
        newUser['userId'], ipAddr, userAgent, token)
    if not tokenSaved:
        return {'error': 'unable to save auth token'}, 500

    # create response to the user
    res = make_response()

    # send token as an http only cookie
    res.set_cookie('auth_token', token, httponly=True)

    # remove password field before sending user data in response
    del user['password']

    # also send token in response body
    res.set_data(json.dumps({"user": user, "token": token}))
    return res, 200


@app.route("/api/v1/auth/logout", methods=["POST"])
@authTokenRequired
@validateTokenSender
@addRequestSenderDataToContext
def handleUserLogout(context={}):
    """
    ENDPOINT: /api/v1/auth/logout
    EXCEPTED METHODS: POST
    """
    userId = context.get('userId', None)
    ipAddr = context.get('ipAddr', None)

    wasDeleted = queryDeleteToken(userId, ipAddr)
    if not wasDeleted:
        return {'error': 'unable to complete logout action'}, 500

    res = make_response()
    res.set_cookie('auth_token', '', httponly=True)
    return res, 200


@app.route("/api/v1/auth/refresh-token", methods=["GET"])
@authTokenRequired
@validateTokenSender
@addRequestSenderDataToContext
def handleRefreshTokenRequest(context={}):
    """
    ENDPOINT: /api/v1/auth/refresh-token
    EXCEPTED METHODS: GET
    """
    userId = context.get('userId', None)

    token = tokenManager.create(userId, 1500)
    if not token:
        return {'error': 'unable to refresh auth token'}, 500

    # save the users tokens
    ipAddr = request.remote_addr
    userAgent = request.user_agent.string
    tokenSaved = queryCreateNewToken(userId, ipAddr, userAgent, token)
    if not tokenSaved:
        return {'error': 'unable to refresh auth token'}, 500

    # create response to the user
    res = make_response()

    # send token as an http only cookie and in response body
    res.set_cookie('auth_token', token, httponly=True)
    res.set_data(json.dumps({"token": token}))
    return res, 200


@app.route("/api/v1/auth/user/<userId>", methods=["GET"])
@authTokenRequired
@addRequestSenderDataToContext
def handleUsernameRequest(userId, context={}):
    """
    ENDPOINT: /api/v1/auth/user/<userId>
    EXCEPTED METHODS: GET
    TODO: Get rid of this route and add userId and username as fields
    for Posts, Responses, and Groups
    """
    username = queryUsernameForUserId(userId)
    if username is None:
        return {'error': 'unable to retrieve username for the given id'}, 500

    return {'username': username}, 200


@app.route("/api/v1/auth/public-key", methods=["GET"])
def handlePublicKeyRequest():
    """
    ENDPOINT: /api/v1/auth/public-key
    EXCEPTED METHODS: GET
    """
    public_key = tokenManager.get_public_key()
    return {'public_key': public_key}, 200


@app.route("/api/v1/auth/health-check", methods=["GET, PUT, POST"])
def handleHealthCheckRequest():
    """
    ENDPOINT: /api/v1/auth/health-check
    EXCEPTED METHODS: GET
    """
    return {}, 200


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
