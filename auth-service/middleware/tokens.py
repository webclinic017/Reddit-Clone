from flask import request, make_response
from utils.tokens import TokenManager
from utils.requests import getAuthTokenFromRequestBody
from db.queries import queryTokenByUserId
import functools


def authTokenRequired(handler):
    """
    Middleware function to ensure the incoming request has an auth_token
    cookie associated with it and that the cookie can successfully decoded
    to yield a userId
    """
    @functools.wraps(handler)
    def wrappedHandler(context={}, *args, **kwargs):
        # First, check for token in request params if get request
        # or request body if POST, PUT, or DELETE
        if request.method == "GET":
            token = request.args.get('token', None)
        else:
            token = getAuthTokenFromRequestBody(request)

        if token is None:
            token = request.cookies.get('auth_token')
            if token is None:
                return {'error': 'missing auth token'}, 400

        # decode the token to get the user id
        tokenManager = TokenManager.get_instance()
        userId = tokenManager.decode(token)
        if not userId:
            return {'error': 'invalid auth token provided'}, 400

        context['token'] = token
        context['userId'] = userId

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
