from flask import Flask, request, make_response
from flask_cors import CORS
from utils.tokens import JsonWebToken
from utils.requests import (
    getLoginCredentialsFromRequest,
    getRegisterCredentialsFromRequest,
)
from utils.hash import checkPasswordMatchesHash, hash
from db.token_storage import TokenStorage
from db.user_storage import UserStorage
from middleware.tokens import (
    authTokenRequired,
    refreshTokenRequired,
    validateRefreshToken,
    allowExpiredAccessToken
)
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
public_key = os.environ.get('TOKEN_PUBLIC_KEY', None)
private_key = os.environ.get('TOKEN_PRIVATE_KEY', None)
jwt = JsonWebToken(public_key, private_key)

# create token database
token_table_name = os.environ.get('TOKEN_DYNAMODB_TABLE_NAME')
aws_region = os.environ.get('AWS_REGION')
token_database = TokenStorage(token_table_name, aws_region)

# create user database
users_table_name = os.environ.get('USER_DYNAMODB_TABLE_NAME')
user_database = UserStorage(users_table_name, aws_region)


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
    email = credentials.get('email')
    user = user_database.query_by_email(email)
    if not user:
        return {"error": "invalid credentials"}, 400

    # check that the provided password matches stored password
    providedPassword = credentials.get('password')
    password = user.get('password')
    if not checkPasswordMatchesHash(providedPassword, password):
        return {"error": "invalid credentials"}, 400

    # Create an access token to identify the user in new requests
    userId = user.get('userId')
    token_data = {'userId': userId, 'tokenType': 'access'}
    twenty_minutes_in_seconds = 60 * 20
    access_token_id, access_token = jwt.create(
        token_data, twenty_minutes_in_seconds)
    if access_token is None:
        return {'error': 'unable to create auth token'}, 500

    # create a refresh token for the user
    token_data = {'userId': userId,
                  'accessTokenId': access_token_id,
                  'tokenType': 'refresh'}
    seven_days_in_seconds = 60 * 60 * 24 * 7
    refresh_token_id, refresh_token = jwt.create(
        token_data, seven_days_in_seconds)
    if refresh_token is None:
        return {'error': 'unable to create refresh token'}, 500

    # save the users access token
    userAgent = context.get('userAgent')
    wasTokenSaved = token_database.save_access_token(
        access_token_id, userId, ipAddr, userAgent)
    if not wasTokenSaved:
        return {'error': 'unable to save auth token'}, 500

    # save the users refresh token
    wasTokenSaved = token_database.save_refresh_token(
        refresh_token_id, userId, access_token_id, ipAddr, userAgent)
    if not wasTokenSaved:
        return {'error': 'unable to save refresh token'}, 500

    # create response to the user
    res = make_response()

    # send token as an http only cookie
    res.set_cookie('refresh_token', refresh_token, httponly=True)

    # remove password field before sending user data in response
    del user['password']

    # also send token in response body
    res.set_data(json.dumps({"user": user, "token": access_token}))
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
    user = user_database.query_by_email(credentials.get('email'))
    if user:
        return {"error": "email already in use"}, 400

    # Hash user password and create new user in the database
    hashedPassword = hash(credentials['password'])
    username = credentials.get('username')
    email = credentials.get('email')
    newUser = user_database.create(username, email, hashedPassword)
    if not newUser:
        return {'error': 'unable to create a new user account'}, 500

    # Create an access token to identify the user in new requests
    userId = user.get('userId')
    token_data = {'userId': userId, 'tokenType': 'access'}
    twenty_minutes_in_seconds = 60 * 20
    access_token_id, access_token = jwt.create(
        token_data, twenty_minutes_in_seconds)
    if access_token is None:
        return {'error': 'unable to create auth token'}, 500

    # create a refresh token for the user
    token_data = {'userId': userId,
                  'accessTokenId': access_token_id,
                  'tokenType': 'refresh'}
    seven_days_in_seconds = 60 * 60 * 24 * 7
    refresh_token_id, refresh_token = jwt.create(
        token_data, seven_days_in_seconds)
    if refresh_token is None:
        return {'error': 'unable to create refresh token'}, 500

    # save the users access token
    userAgent = context.get('userAgent')
    ipAddr = context.get('ipAddr')
    wasTokenSaved = token_database.save_access_token(
        access_token_id, userId, ipAddr, userAgent)
    if not wasTokenSaved:
        return {'error': 'unable to save auth token'}, 500

    # save the users refresh token
    wasTokenSaved = token_database.save_refresh_token(
        refresh_token_id, userId, access_token_id, ipAddr, userAgent)
    if not wasTokenSaved:
        return {'error': 'unable to save refresh token'}, 500

    # create response to the user
    res = make_response()

    # send token as an http only cookie
    res.set_cookie('refresh_token', refresh_token, httponly=True)

    # also send token in response body
    res.set_data(json.dumps({"user": user, "token": access_token}))
    return res, 200


@app.route("/api/v1/auth/logout", methods=["POST"])
@authTokenRequired
@refreshTokenRequired
@addRequestSenderDataToContext
def handleUserLogout(context={}):
    """
    ENDPOINT: /api/v1/auth/logout
    EXCEPTED METHODS: POST
    """
    userId = context.get('userId')
    refreshToken = context.get('refreshToken')
    accessToken = context.get('accessToken')

    didDeleteAccessToken = token_database.delete(
        accessToken['tokenId'], userId)
    if not didDeleteAccessToken:
        return {'error': 'could not revoke access token'}, 400

    didDeleteRefreshToken = token_database.delete(
        refreshToken['tokenId'], userId)
    if not didDeleteRefreshToken:
        return {'error': 'could not revoke refresh token'}, 400

    res = make_response()
    res.set_cookie('refresh_token', '', httponly=True)
    return res, 200


@app.route("/api/v1/auth/refresh-token", methods=["POST"])
@allowExpiredAccessToken
@refreshTokenRequired
@validateRefreshToken
@addRequestSenderDataToContext
def handleRefreshTokenRequest(context={}):
    """
    ENDPOINT: /api/v1/auth/refresh-token
    EXCEPTED METHODS: GET
    """
    refreshToken = context.get('refreshToken')
    userId = refreshToken.get('userId', None)
    accessTokenId = refreshToken.get('accessTokenId')

    didDeleteAccessToken = token_database.delete(accessTokenId, userId)
    if not didDeleteAccessToken:
        return {'error': 'could not revoke access token'}, 400

    didDeleteRefreshToken = token_database.delete(
        refreshToken['tokenId'], userId)
    if not didDeleteRefreshToken:
        return {'error': 'could not revoke access token'}, 400

    # Create an access token to identify the user in new requests
    token_data = {'userId': userId, 'tokenType': 'access'}
    twenty_minutes_in_seconds = 60 * 20
    access_token_id, access_token = jwt.create(
        token_data, twenty_minutes_in_seconds)
    if access_token is None:
        return {'error': 'unable to create auth token'}, 500

    # create a refresh token for the user
    token_data = {'userId': userId,
                  'accessTokenId': access_token_id,
                  'tokenType': 'refresh'}
    seven_days_in_seconds = 60 * 60 * 24 * 7
    refresh_token_id, refresh_token = jwt.create(
        token_data, seven_days_in_seconds)
    if refresh_token is None:
        return {'error': 'unable to create refresh token'}, 500

    # save the users access token
    userAgent = context.get('userAgent')
    ipAddr = context.get('ipAddr')
    wasTokenSaved = token_database.save_access_token(
        access_token_id, userId, ipAddr, userAgent)
    if not wasTokenSaved:
        return {'error': 'unable to save auth token'}, 500

    # save the users refresh token
    wasTokenSaved = token_database.save_refresh_token(
        refresh_token_id, userId, access_token_id, ipAddr, userAgent)
    if not wasTokenSaved:
        return {'error': 'unable to save refresh token'}, 500

    # create response to the user
    res = make_response()

    # send token as an http only cookie
    res.set_cookie('refresh_token', refresh_token, httponly=True)

    # also send token in response body
    res.set_data(json.dumps({"token": access_token}))
    return res, 200


@app.route("/api/v1/auth/public-key", methods=["GET"])
@authTokenRequired
def handlePublicKeyRequest():
    """
    ENDPOINT: /api/v1/auth/public-key
    EXCEPTED METHODS: GET
    """
    public_key = jwt.get_public_key()
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
