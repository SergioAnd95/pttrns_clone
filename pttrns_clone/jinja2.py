import re

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.utils import translation
from django.utils.translation import get_language, get_language_info
from django.conf import settings

from jinja2 import Environment


def strip_lang(path):
    pattern = '^(/%s)/' % get_language()
    match = re.search(pattern, path)
    if match is None:
        return path
    return path[match.end(1):]

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'get_current_language': get_language,
        'get_available_languages': lambda : settings.LANGUAGES,
        'get_language_info_list': lambda arr: [get_language_info(i[0]) for i in arr],
        'strip_lang': strip_lang
    })

    env.install_gettext_translations(translation)
    return env