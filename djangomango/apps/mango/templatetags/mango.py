import os
import scss as pyscss
import coffeescript
import logging

from django.conf import settings
from django.template.base import Library
from django.contrib.staticfiles.templatetags.staticfiles import static


STATIC_ROOT = os.path.join(settings.PROJECT_DIR, 'static')

logger = logging.getLogger('generic')
register = Library()


def _init_scss():
    """ Initialize pyScss. """
    pyscss.STATIC_ROOT = STATIC_ROOT
    pyscss.STATIC_URL = settings.STATIC_URL
    pyscss.LOAD_PATHS = settings.SCSS_LOAD_PATHS

    return pyscss.Scss(scss_opts=settings.SCSS_OPTIONS)


@register.simple_tag
def scss(path):
    """ Template tag to compile scss files if needed and return its url. """

    # FIXME: init once
    _scss = _init_scss()

    filename = '%s.css' % os.path.splitext(path)[0]
    scss_file = os.path.join(STATIC_ROOT, path)
    css_file = os.path.join(STATIC_ROOT, filename)

    if not os.path.isfile(css_file):
        css_mtime = -1
    else:
        css_mtime = os.path.getmtime(css_file)

    if os.path.getmtime(scss_file) >= css_mtime:
        try:
            compiled = _scss.compile(open(scss_file).read())
            with open(css_file, 'w') as f:
                f.write(compiled)
            logger.info('Compiled scss file: %s' % scss_file)
        except Exception as e:
            logger.debug("Can't compile scss file: %s" % scss_file)
            logger.debug(e)

    return static(filename)


@register.simple_tag
def coffee(path):
    """
    Template tag to compile coffeescript files if needed and return its url.
    """
    filename = 'js/%s.js' % os.path.splitext(os.path.basename(path))[0]
    coffee_file = os.path.join(STATIC_ROOT, path)
    js_file = os.path.join(STATIC_ROOT, filename)

    if not os.path.isfile(js_file):
        js_mtime = -1
    else:
        js_mtime = os.path.getmtime(js_file)

    if os.path.getmtime(coffee_file) >= js_mtime:
        try:
            compiled = coffeescript.compile(open(coffee_file).read())
            with open(js_file, 'w') as f:
                f.write(compiled)
            logger.info('Compiled coffee script file: %s' % coffee_file)
        except Exception as e:
            logger.debug("Can't compile coffee script file: %s" % coffee)
            logger.debug(e)

    return static(filename)


@register.filter
def in_group(user, groups):
    """ Checks if user is member of groups. """
    return bool(user.groups.filter(name__in=groups.split(',')).values('name'))
