from flask import request
import functools


def addRequestSenderDataToContext(handler):
    """
    """
    @functools.wraps(handler)
    def wrappedHandler(context={}, *args, **kwargs):

        context['ipAddr'] = request.remote_addr
        context['userAgent'] = request.user_agent.string

        return handler(context=context, *args, **kwargs)
    return wrappedHandler
