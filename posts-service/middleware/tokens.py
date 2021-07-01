from flask import request
from utils.tokens import getUserIdFromToken
import functools


def authTokenRequired(handler):
    """
    Middleware function to ensure the incoming request has an auth_token
    cookie associated with it and that the cookie can successfully decoded
    to yield a userId
    """
    @functools.wraps(handler)
    def wrappedHandler(context={}, *args, **kwargs):
        # check that a token cookie is present
        token = request.cookies.get('auth_token')
        if not token:
            return {'error': 'missing auth token'}, 400

        # decode the token to get the user id
        userId = getUserIdFromToken(token)
        if not userId:
            return {'error': 'invalid auth token provided'}, 400

        context['token'] = token
        context['userId'] = userId

        return handler(context=context, *args, **kwargs)
    return wrappedHandler
