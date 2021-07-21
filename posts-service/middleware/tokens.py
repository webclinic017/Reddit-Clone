from flask import request
from utils.tokens import getUserIdFromToken
from utils.requests import getAuthTokenFromRequestBody
import functools


def authTokenRequired(handler):
    """
    Middleware function to ensure the incoming request has an auth_token
    cookie associated with it and that the cookie can successfully decoded
    to yield a userId
    """
    @functools.wraps(handler)
    def wrappedHandler(context={}):
        # First, check for token in request params if get request
        # or request body if POST, PUT, or DELETE
        if request.method == "GET":
            token = request.args.get('token', None)
        else:
            token = getAuthTokenFromRequestBody(request)

        # if token not found in body, check for cookie
        if token is None:
            token = request.cookies.get('auth_token')
            if token is None:
                return {'error': 'missing auth token'}, 400

        # decode the token to get the user id
        userId = getUserIdFromToken(token)
        if not userId:
            return {'error': 'invalid auth token provided'}, 400

        context['token'] = token
        context['userId'] = userId

        return handler(context=context)
    return wrappedHandler
