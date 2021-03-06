import re
import os
import scss as pyscss
import coffeescript
import logging
import fnmatch
import tempfile

from django.conf import settings
from django.template.base import Library
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles import finders
from django.template.base import TemplateSyntaxError

from .settings import (STATIC_ROOT, STATIC_URL, LOAD_PATHS, ASSETS_ROOT,
                       ASSETS_URL, SCSS_COMPRESS, SCSS_DEBUG_INFO,
                       SCSS_REBUILD, COFFEE_OUTPUT, COFFEE_REBUILD,
                       LESS_REBUILD)


logger = logging.getLogger('assetstoolkit')
register = Library()

STATIC_PATTERN = re.compile(r'url\(\{\% static (.*) \%\}\)')


def finder(glob):
    """
    Finds all files in the django finders for a given glob,
    returns the file path, if available, and the django storage object.
    storage objects must implement the File storage API:
    https://docs.djangoproject.com/en/dev/ref/files/storage/
    """
    for finder in finders.get_finders():
        for path, storage in finder.list([]):
            if fnmatch.fnmatchcase(path, glob):
                yield path, storage


def memoize_scss(func):
    cache = {}

    def wrapper():
        if not cache.get('scss', None):
            cache['scss'] = func()
        return cache['scss']
    return wrapper


def context_match(matchobj):
    uri = matchobj.group(1)
    uri = uri.strip(' \'"')
    return "url('%s')" % static(uri)


def create_tmp_file(static_file):
    """
    Look for static template tag on the less file
    and fetch the full url by passing it to static.
    """
    with open(static_file, 'r') as handle:
        static_content = STATIC_PATTERN.sub(context_match, handle.read())

        # create the temporary file as sibling of original file
        # so any mixin import (in case of less/sass) can be found.
        tmp_file = tempfile.NamedTemporaryFile(
            delete=False, dir=os.path.dirname(static_file))
        tmp_file.write(static_content)
        tmp_file.close()
        return tmp_file


@memoize_scss
def _init_scss():
    """ Initialize pyScss. """
    pyscss.STATIC_ROOT = finder
    pyscss.STATIC_URL = STATIC_URL
    pyscss.LOAD_PATHS = LOAD_PATHS
    pyscss.ASSETS_ROOT = ASSETS_ROOT
    pyscss.ASSETS_URL = ASSETS_URL

    scss_opts = {'compress': SCSS_COMPRESS, 'debug_info': SCSS_DEBUG_INFO}
    return pyscss.Scss(scss_opts=scss_opts)


@register.simple_tag
def scss(path):
    """ Compile scss file if needed and return its url. """

    _scss = _init_scss()

    filename = '%s.css' % os.path.splitext(path)[0]
    scss_file = get_asset_path(path)
    css_file = os.path.join(os.path.dirname(scss_file),
                            os.path.basename(filename))

    if not os.path.isfile(css_file):
        css_mtime = -1
    else:
        css_mtime = os.path.getmtime(css_file)

    if SCSS_REBUILD:
        if os.path.getmtime(scss_file) >= css_mtime:
            tmp_file = create_tmp_file(scss_file)

            try:
                compiled = _scss.compile(open(tmp_file).read())
                with open(css_file, 'w') as f:
                    f.write(compiled)
                logger.info('Compiled scss file: %s' % scss_file)
            except Exception as e:
                logger.debug("Can't compile scss file: %s" % scss_file)
                logger.debug(e)

            # remove temporary file
            os.unlink(tmp_file.name)

    return static(filename)


@register.simple_tag
def less(path):
    """ Compile less file if needed and return its url. """

    filename = '%s.css' % os.path.splitext(path)[0]
    less_file = get_asset_path(path)
    css_file = os.path.join(os.path.dirname(less_file),
                            os.path.basename(filename))

    if not os.path.isfile(css_file):
        css_mtime = -1
    else:
        css_mtime = os.path.getmtime(css_file)

    if LESS_REBUILD:
        if os.path.getmtime(less_file) >= css_mtime:
            tmp_file = create_tmp_file(less_file)

            try:
                os.system('lessc %(from)s > %(to)s -x' %
                          {'from': tmp_file.name, 'to': css_file})
                logger.info('Compiled less file: %s' % less_file)
            except Exception as e:
                logger.debug("Can't compile less file: %s" % less_file)
                logger.debug(e)

            # remove temporary file
            os.unlink(tmp_file.name)

    return static(filename)


@register.simple_tag
def coffee(path):
    """ Compile coffeescript file if needed and return its url. """

    filename = '%s.js' % os.path.splitext(os.path.basename(path))[0]
    coffee_file = get_asset_path(path)

    segments = path.split(os.sep)[1:-1]
    segments.append(filename)
    js_filename = os.path.join(COFFEE_OUTPUT, *segments)
    js_file = coffee_file.replace(path, js_filename)

    if not os.path.isfile(js_file):
        js_mtime = -1
    else:
        js_mtime = os.path.getmtime(js_file)

    if COFFEE_REBUILD:
        if os.path.getmtime(coffee_file) >= js_mtime:
            try:
                compiled = coffeescript.compile(open(coffee_file).read())
                with open(js_file, 'w') as f:
                    f.write(compiled)
                logger.info('Compiled coffee script file: %s' % coffee_file)
            except Exception as e:
                logger.debug("Can't compile coffee script file: %s" % coffee)
                logger.debug(e)

    return static(js_filename)


def get_asset_path(path):
    full_path = os.path.join(STATIC_ROOT, path)
    if settings.DEBUG and not os.path.exists(full_path):
        full_path = finders.find(path)

        if full_path is None:
            raise TemplateSyntaxError("Can't find staticfile named: %s" % path)

    return full_path
