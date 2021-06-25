def containsNewGroupFields(group: dict) -> bool:
    """
    Function to determine if the groups dictionary contains the
    required fields
    """
    if not group:
        return False

    if 'name' not in group or 'description' not in group:
        return False

    return True


def getCreateGroupFieldsFromRequest(request):
    """
    Function to retrieve the field to create a new group
    from the flask request
    """
    if request is None:
        return None

    body = request.get_json(force=True)
    if not body or 'group' not in body:
        return None

    group = body['group']
    if not containsNewGroupFields(group):
        return None

    return group
