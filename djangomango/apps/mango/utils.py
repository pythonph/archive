import os
import shutil

from django.conf import settings


def moderator_required(user):
    """ Check if user accessing is a moderator. """
    if user.is_authenticated() and user.groups.filter(name='moderator'):
        return True
    return False


def get_mugshots_path(instance, filename):
    """ Return mugshot path relative to MEDIA_ROOT. """
    mugshot_path = os.path.join('mugshots', str(instance.user.id))
    abs_mugshot_path = os.path.join(settings.MEDIA_ROOT, mugshot_path)

    # create mugshots path if it doesn't exist yet
    if not os.path.exists(abs_mugshot_path):
        os.makedirs(abs_mugshot_path)

    return os.path.join(mugshot_path, filename)
