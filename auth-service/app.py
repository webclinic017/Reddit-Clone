from flask import Flask, request, make_response
from flask_cors import CORS
from utils.tokens import createJWT
from utils.requests import (
    getLoginCredentialsFromRequest,
    getRegisterCredentialsFromRequest
)
from utils.hash import checkPasswordMatchesHash, hash
from db.queries import (
    queryUserByEmail,
    queryCreateNewUser,
    queryCreateNewToken,
    queryDeleteToken,
    queryUsernameForUserId
)
from middleware.tokens import authTokenRequired, validateTokenSender
import os
import json

# Create a new Flask app
app = Flask(__name__)

# Set up CORS
CORS(app, resources={r"/*": {"origins": "*"}})


##########################################################
# ENDPOINT: /api/v1/auth/login
# EXCEPTED METHODS: POST
#
#
##########################################################
@app.route("/api/v1/auth/login", methods=["POST"])
def handleUserLogin():
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

    # Create a JWT to identify the user in new requests
    userId = user['userId']
    token = createJWT(userId)
    if not token:
        return {'error': 'unable to create auth token'}, 500

    # save the users tokens
    ipAddr = request.remote_addr
    userAgent = request.user_agent.string
    tokenSaved = queryCreateNewToken(userId, ipAddr, userAgent, token)
    if not tokenSaved:
        return {'error': 'unable to save auth token'}, 500

    # send response to the user
    res = make_response()
    res.set_cookie('auth_token', token, httponly=True)
    del user['password']
    res.set_data(json.dumps({"user": user, "token": token}))
    return res, 200


##########################################################
# ENDPOINT: /api/v1/auth/register
# EXCEPTED METHODS: POST
#
#
##########################################################
@app.route("/api/v1/auth/register", methods=["POST"])
def handleUserRegister():
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
    token = createJWT(newUser['userId'])
    if not token:
        return {'error': 'unable to create auth token'}, 500

    # save the users tokens
    ipAddr = request.remote_addr
    userAgent = request.user_agent.string
    tokenSaved = queryCreateNewToken(
        newUser['userId'], ipAddr, userAgent, token)
    if not tokenSaved:
        return {'error': 'unable to save auth token'}, 500

    res = make_response()
    res.set_cookie('auth_token', token, httponly=True)
    return {"user": newUser, "token": token}, 200


##########################################################
# ENDPOINT: /api/v1/auth/logout
# EXCEPTED METHODS: POST
#
#
##########################################################
@app.route("/api/v1/auth/logout", methods=["POST"])
@authTokenRequired
@validateTokenSender
def handleUserLogout(context={}):
    userId = context.get('userId', None)

    wasDeleted = queryDeleteToken(userId)
    if not wasDeleted:
        return {'error': 'unable to complete logout action'}, 500

    res = make_response()
    res.set_cookie('auth_token', '', httponly=True)
    return res, 200


##########################################################
# ENDPOINT: /api/v1/auth/refresh-token
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route("/api/v1/auth/refresh-token", methods=["GET"])
@authTokenRequired
@validateTokenSender
def handleRefreshTokenRequest(context={}):
    userId = context.get('userId', None)

    token = createJWT(userId)
    if not token:
        return {'error': 'unable to refresh auth token'}, 500

    # save the users tokens
    ipAddr = request.remote_addr
    userAgent = request.user_agent.string
    tokenSaved = queryCreateNewToken(userId, ipAddr, userAgent, token)
    if not tokenSaved:
        return {'error': 'unable to refresh auth token'}, 500

    res = make_response()
    res.set_cookie('auth_token', token, httponly=True)
    return res, 200


##########################################################
# ENDPOINT: /api/v1/auth/public-key
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route("/api/v1/auth/public-key", methods=["GET"])
def handlePublicKeyRequest():
    public_key = os.environ.get('TOKEN_PUBLIC_KEY')
    return {'public_key': public_key}, 200


##########################################################
# ENDPOINT: /api/v1/auth/health-check
# EXCEPTED METHODS: GET
#
#
##########################################################
@app.route("/api/v1/auth/health-check", methods=["GET, PUT, POST"])
def handleHealthCheckRequest():
    return {}, 200


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
