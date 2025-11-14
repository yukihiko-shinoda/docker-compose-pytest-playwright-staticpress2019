"""SQLAlchemy entity models for WordPress database tables. These models replace the TypeORM entities from the
TypeScript version.

Note: These entities are optional since the codebase uses raw SQL queries.
They are provided for reference and potential future use.
"""

from .wp_option import Base
from .wp_option import WpOption
from .wp_post import WpPost
from .wp_user import WpUser

__all__ = [
    "Base",
    "WpOption",
    "WpPost",
    "WpUser",
]
