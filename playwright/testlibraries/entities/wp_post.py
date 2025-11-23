"""WordPress wp_posts table entity model.

This replaces WpPost.ts from the TypeScript version.
"""

from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from .wp_option import Base


class WpPost(Base):
    """WordPress posts table model.

    This replaces the TypeScript TypeORM entity from WpPost.ts.

    Note: This entity is provided for reference. The actual implementation
    uses raw SQL queries via config.get_db_connection() instead of the ORM.
    """

    __tablename__ = "wp_posts"
    __table_args__ = (
        Index("post_name", "post_name"),
        Index("type_status_date", "post_type", "post_status", "post_date", "ID"),
        Index("post_parent", "post_parent"),
        Index("post_author", "post_author"),
        {"schema": "exampledb"},
    )

    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    post_author = Column(BigInteger, default=0, nullable=False)
    post_date = Column(DateTime, default=datetime(1000, 1, 1, 0, 0, 0), nullable=False)
    post_date_gmt = Column(DateTime, default=datetime(1000, 1, 1, 0, 0, 0), nullable=False)
    post_content = Column(Text, nullable=False)
    post_title = Column(Text, nullable=False)
    post_excerpt = Column(Text, nullable=False)
    post_status = Column(String(20), default="publish", nullable=False)
    comment_status = Column(String(20), default="open", nullable=False)
    ping_status = Column(String(20), default="open", nullable=False)
    post_password = Column(String(255), nullable=False)
    post_name = Column(String(200), nullable=False)
    to_ping = Column(Text, nullable=False)
    pinged = Column(Text, nullable=False)
    post_modified = Column(DateTime, default=datetime(1000, 1, 1, 0, 0, 0), nullable=False)
    post_modified_gmt = Column(DateTime, default=datetime(1000, 1, 1, 0, 0, 0), nullable=False)
    post_content_filtered = Column(Text, nullable=False)
    post_parent = Column(BigInteger, default=0, nullable=False)
    guid = Column(String(255), nullable=False)
    menu_order = Column(Integer, default=0, nullable=False)
    post_type = Column(String(20), default="post", nullable=False)
    post_mime_type = Column(String(100), nullable=False)
    comment_count = Column(BigInteger, default=0, nullable=False)

    def __repr__(self) -> str:
        """String representation of the WpPost model."""
        return f"<WpPost(ID={self.ID}, post_title='{self.post_title[:50]}...', post_type='{self.post_type}')>"
