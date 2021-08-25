from flask import request, make_response
from utils.tokens import JsonWebToken
from utils.requests import getAuthTokenFromRequestBody
from db.token_storage import TokenStorage
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


def allowExpiredAccessToken(handler):
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
        payload = jwt.decode_without_verification(token)
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
        context['userId'] = payload.get('userId')

        return handler(context=context, *args, **kwargs)
    return wrappedHandler


def validateRefreshToken(handler):
    """
    Middleware function to validate
    """
    @functools.wraps(handler)
    def wrappedHandler(context={}, *args, **kwargs):
        # ensure that we have a token in the current context
        refresh_token = context.get('refreshToken', None)
        if not refresh_token:
            return {'error': 'invalid or missing refresh token'}, 400

        access_token = context.get('accessToken')
        if access_token is None:
            return {'error': 'missing access token'}, 400

        # ensure that we have a userId in the current context
        userId = refresh_token.get('userId', None)
        if not userId:
            return {'error': 'invalid or missing refresh token'}, 400

        # get the token id from the token payload
        tokenId = refresh_token.get('tokenId', None)
        if tokenId is None:
            return {'error': 'invalid or missing refresh token'}, 400

        # retrieve saved token from the database
        token_database = TokenStorage.get_instance()
        saved_refresh_token = token_database.query(tokenId, userId)
        if not saved_refresh_token:
            return {'error': 'no token saved for given user id'}, 400

        # check that token is coming from same user
        hasSameIpAddr = saved_refresh_token['ipAddr'] == request.remote_addr
        hasSameUserAgent = saved_refresh_token['userAgent'] == request.user_agent.string
        hasSameTokenId = saved_refresh_token['tokenId'] == tokenId

        # check that refresh token matches access token
        access_token_id = access_token.get('tokenId')
        isValidTokenPair = access_token_id == refresh_token.get(
            'accessTokenId')

        if not hasSameIpAddr or not hasSameUserAgent or not hasSameTokenId or not isValidTokenPair:
            # delete the users access and refresh tokens
            token_database.delete(tokenId, userId)
            token_database.delete(refresh_token.get('accessTokenId'), userId)
            errMessage = {
                'error': 'could not validate token sender. token revoked'
            }
            res = make_response(errMessage, 403)
            res.set_cookie('refresh_token', '', httponly=True)
            return res

        return handler(context=context, *args, **kwargs)
    return wrappedHandler
