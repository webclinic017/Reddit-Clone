def getGroupNameFromRequestBody(request):
    if request is None:
        return None

    body = request.get_json(force=True)
    if body is None or 'groupName' not in body:
        return None

    return body['groupName']


def containsValidPostData(post):
    if post is None:
        return False

    containsPost = 'post' in post
    containsTitle = 'title' in post
    containsGroupName = 'groupName' in post
    if not containsPost or not containsGroupName or not containsTitle:
        return False

    return True


def getPostFromRequestBody(request):
    if request is None:
        return None

    body = request.get_json(force=True)
    if body is None or 'post' not in body:
        return None

    post = body['post']
    if not containsValidPostData(post):
        return None

    return body['post']


def getResponseFromRequestBody(request):
    if request is None:
        return None

    body = request.get_json(force=True)
    if body is None or 'response' not in body:
        return None

    response = body['response']
    return response


def getAuthTokenFromRequestBody(request):
    body = request.get_json(force=True)
    if not body or 'token' not in body:
        return None

    return body['token']
