
def moderator_required(user):
    """ Check if user accessing is a moderator. """
    if user.is_authenticated() and user.groups.filter(name='moderator'):
        return True
    return False
