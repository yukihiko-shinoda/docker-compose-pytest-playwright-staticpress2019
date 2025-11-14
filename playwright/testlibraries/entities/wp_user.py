"""WordPress wp_users table entity model.

This replaces WpUser.ts from the TypeScript version.
"""

from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String

from .wp_option import Base


class WpUser(Base):
    """WordPress users table model.

    This replaces the TypeScript TypeORM entity from WpUser.ts.

    Note: This entity is provided for reference. The actual implementation
    uses raw SQL queries via config.get_db_connection() instead of the ORM.
    """

    __tablename__ = "wp_users"
    __table_args__ = (
        Index("user_login_key", "user_login"),
        Index("user_nicename", "user_nicename"),
        Index("user_email", "user_email"),
        {"schema": "exampledb"},
    )

    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    user_login = Column(String(60), nullable=False)
    user_pass = Column(String(255), nullable=False)
    user_nicename = Column(String(50), nullable=False)
    user_email = Column(String(100), nullable=False)
    user_url = Column(String(100), nullable=False)
    user_registered = Column(DateTime, default=datetime(1000, 1, 1, 0, 0, 0), nullable=False)
    user_activation_key = Column(String(255), nullable=False)
    user_status = Column(Integer, default=0, nullable=False)
    display_name = Column(String(250), nullable=False)

    def __repr__(self) -> str:
        """String representation of the WpUser model."""
        return f"<WpUser(ID={self.ID}, user_login='{self.user_login}', user_email='{self.user_email}')>"
