def getGroupIdFromRequestBody(request):
    if request is None:
        return None

    body = request.get_json(force=True)
    if body is None or 'groupId' not in body:
        return None

    return body['groupId']


def containsValidPostData(post):
    if post is None:
        return False

    containsPost = 'post' in post
    containsGroupId = 'groupId' in post
    if not containsPost or not containsGroupId:
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
