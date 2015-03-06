import os
import shutil

from django.conf import settings


def get_mugshots_path(instance, filename):
    """ Return mugshot path relative to MEDIA_ROOT. """
    mugshot_path = os.path.join('mugshots', str(instance.user.id))
    abs_mugshot_path = os.path.join(settings.MEDIA_ROOT, mugshot_path)

    # create mugshots path if it doesn't exist yet
    if not os.path.exists(abs_mugshot_path):
        os.makedirs(abs_mugshot_path)

    return os.path.join(mugshot_path, filename)
