def containsLoginCredentials(creds: dict) -> bool:
    """
    helper function to check that required login credential fields
    have been provided
    """
    if not creds:
        return False

    if 'email' not in creds or 'password' not in creds:
        return False

    return True


def containsRegisterCredentials(creds: dict) -> bool:
    """
    helper function to check that required register credential fields
    have been provided
    """
    if not containsLoginCredentials(creds):
        return False

    if 'username' not in creds:
        return False

    return True


def getLoginCredentialsFromRequest(request):
    """
    helper function to retrieve login credentials from flask request object
    """
    body = request.get_json(force=True)
    if not body or 'user' not in body:
        return None

    credentials = body['user']
    if not containsLoginCredentials(credentials):
        return None

    return credentials


def getRegisterCredentialsFromRequest(request):
    """
    helper function to retrieve register credentials from flask request object
    """
    body = request.get_json(force=True)
    if not body or 'user' not in body:
        return None

    credentials = body['user']
    if not containsRegisterCredentials(credentials):
        return None

    return credentials


def getAuthTokenFromRequestBody(request):
    body = request.get_json(force=True)
    if not body or 'token' not in body:
        return None

    return body['token']
