from flask import request, make_response
from utils.tokens import JsonWebToken
from utils.requests import getAuthTokenFromRequestBody
from db.dynamodb_token_storage import DynamoDBTokenStorage
import functools


def authTokenRequired(handler):
    """
    Middleware function to ensure the incoming request has an auth_token
    cookie associated with it and that the cookie can successfully decoded
    to yield a userId
    """
    @functools.wraps(handler)
    def wrappedHandler(context={}, *args, **kwargs):
        # check for token in request params if get request
        # or request body if POST, PUT, or DELETE
        if request.method == "GET":
            token = request.args.get('accessToken', None)
        else:
            token = getAuthTokenFromRequestBody(request)

        if token is None:
            return {'error': 'missing auth token'}, 400

        # decode the token to get the user id
        jwt = JsonWebToken.get_instance()
        payload = jwt.decode(token)
        if not payload:
            return {'error': 'invalid auth token provided'}, 400

        context['accessToken'] = payload
        context['userId'] = payload.get('userId')

        return handler(context=context, *args, **kwargs)
    return wrappedHandler


def refreshTokenRequired(handler):
    """
    Middleware function to ensure the incoming request has a valid
    refresh_token cookie associated
    """
    @functools.wraps(handler)
    def wrappedHandler(context={}, *args, **kwargs):
        token = request.cookies.get('refresh_token')
        if token is None:
            return {'error': 'missing refresh token'}, 400

        # decode the token to get the user id
        jwt = JsonWebToken.get_instance()
        payload = jwt.decode(token)
        if payload is None:
            return {'error': 'invalid refresh token provided'}, 400

        context['refreshToken'] = payload

        return handler(context=context, *args, **kwargs)
    return wrappedHandler


def validateTokenSender(handler):
    """
    Middleware function to validate that the auth_token cookie received
    is associated with a valid userId. The middleware will check that the
    IP address, user agent are the same as when the token was issued. Function
    will also check that the token has not been modified since issued.
    """
    @functools.wraps(handler)
    def wrappedHandler(context={}, *args, **kwargs):
        # ensure that we have a token in the current context
        receivedToken = context.get('token', None)
        if not receivedToken:
            return {'error': 'invalid or missing auth token'}, 400

        # ensure that we have a userId in the current context
        userId = context.get('userId', None)
        if not userId:
            return {'error': 'invalid or missing auth token'}, 400

        savedToken = queryTokenByUserId(userId, request.remote_addr)
        if not savedToken:
            return {'error': 'no token saved for given user id'}, 400

        hasSameIpAddr = savedToken['ipAddr'] == request.remote_addr
        hasSameUserAgent = savedToken['userAgent'] == request.user_agent.string
        isSameToken = receivedToken == savedToken['token']

        if not hasSameIpAddr or not hasSameUserAgent or not isSameToken:
            errMessage = {
                'error': 'could not validate token sender. token revoked'
            }
            res = make_response(errMessage, 403)
            res.set_cookie('auth_token', '', httponly=True)
            return res

        return handler(context=context, *args, **kwargs)
    return wrappedHandler


def validateRefreshToken(handler):
    """
    Middleware function to validate
    """
    @functools.wraps(handler)
    def wrappedHandler(context={}, *args, **kwargs):
        # ensure that we have a token in the current context
        receivedToken = context.get('refreshToken', None)
        if not receivedToken:
            return {'error': 'invalid or missing refresh token'}, 400

        # ensure that we have a userId in the current context
        userId = receivedToken.get('userId', None)
        if not userId:
            return {'error': 'invalid or missing refresh token'}, 400

        # get the token id from the token payload
        tokenId = receivedToken.get('tokenId', None)
        if tokenId is None:
            return {'error': 'invalid or missing refresh token'}, 400

        # retrieve saved token from the database
        token_database = DynamoDBTokenStorage.get_instance()
        savedToken = token_database.query(tokenId, userId)
        if not savedToken:
            return {'error': 'no token saved for given user id'}, 400

        # check that token is coming from same user
        hasSameIpAddr = savedToken['ipAddr'] == request.remote_addr
        hasSameUserAgent = savedToken['userAgent'] == request.user_agent.string
        hasSameTokenId = savedToken['tokenId'] == tokenId

        if not hasSameIpAddr or not hasSameUserAgent or not hasSameTokenId:
            errMessage = {
                'error': 'could not validate token sender. token revoked'
            }
            res = make_response(errMessage, 403)
            res.set_cookie('refresh_token', '', httponly=True)
            return res

        return handler(context=context, *args, **kwargs)
    return wrappedHandler
