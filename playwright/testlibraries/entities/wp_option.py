"""WordPress wp_options table entity model.

This replaces WpOption.ts from the TypeScript version.
"""

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


class WpOption(Base):
    """WordPress options table model.

    This replaces the TypeScript TypeORM entity:
    ```typescript
    @Index("option_name", ["optionName"], { unique: true })
    @Index("autoload", ["autoload"], {})
    @Entity("wp_options", { schema: "exampledb" })
    export class WpOption {
      @PrimaryGeneratedColumn({ type: "bigint", name: "option_id", unsigned: true })
      optionId!: string;

      @Column("varchar", { name: "option_name", unique: true, length: 191 })
      optionName!: string;

      @Column("longtext", { name: "option_value" })
      optionValue!: string;

      @Column("varchar", { name: "autoload", length: 20, default: () => "'yes'" })
      autoload!: string;
    }
    ```

    Note: This entity is provided for reference. The actual implementation
    uses raw SQL queries via config.get_db_connection() instead of the ORM.
    """

    __tablename__ = "wp_options"
    __table_args__ = (
        Index("option_name", "option_name", unique=True),
        Index("autoload", "autoload"),
        {"schema": "exampledb"},
    )

    option_id = Column(BigInteger, primary_key=True, autoincrement=True)
    option_name = Column(String(191), unique=True, nullable=False)
    option_value = Column(Text, nullable=False)
    autoload = Column(String(20), default="yes", nullable=False)

    def __repr__(self) -> str:
        """String representation of the WpOption model."""
        return f"<WpOption(option_name='{self.option_name}', option_value='{self.option_value[:50]}...')>"
