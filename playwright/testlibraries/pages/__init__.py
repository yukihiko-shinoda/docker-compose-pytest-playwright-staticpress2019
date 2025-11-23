"""Page Object Models for WordPress and StaticPress pages.

These models replace the TypeScript page objects from the TypeScript version.
"""

from .page_admin import PageAdmin
from .page_language_chooser import PageLanguageChooser
from .page_login import PageLogin
from .page_plugins import PagePlugins
from .page_staticpress import PageStaticPress
from .page_staticpress_options import PageStaticPressOptions
from .page_welcome import PageWelcome

__all__ = [
    "PageAdmin",
    "PageLanguageChooser",
    "PageLogin",
    "PagePlugins",
    "PageStaticPress",
    "PageStaticPressOptions",
    "PageWelcome",
]
