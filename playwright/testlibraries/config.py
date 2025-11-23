"""Database configuration for SQLAlchemy.

This replaces ormconfig.ts from the TypeScript version.
"""

import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

load_dotenv()

# Database connection parameters
DATABASE_CONFIG = {
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": 3306,
    "username": "exampleuser",
    "password": "examplepass",
    "database": "exampledb",
}

# SQLAlchemy connection URL
DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)

# SQLAlchemy engine options
ENGINE_OPTIONS = {
    "echo": False,  # Set to True for SQL logging
    "pool_pre_ping": True,  # Verify connections before using
    "pool_recycle": 3600,  # Recycle connections after 1 hour
}


@contextmanager
def get_db_connection() -> Connection:
    """Context manager for database connections.

    This replaces the TypeORM DataSource pattern:
    ```typescript
    let connection;
    try {
      const myDataSource = new DataSource(ormconfig);
      connection = await myDataSource.initialize();
      // ... operations
    } finally {
      if (connection) {
        await connection.destroy();
      }
    }
    ```

    Usage:
    ```python
    with get_db_connection() as conn:
        result = conn.execute(text("SELECT * FROM wp_options"))
    ```

    Yields:
        Connection: SQLAlchemy connection object
    """
    engine: Engine = create_engine(DATABASE_URL, **ENGINE_OPTIONS)
    connection: Connection = engine.connect()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
        engine.dispose()
