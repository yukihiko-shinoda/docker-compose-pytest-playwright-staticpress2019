"""Table cleaner for StaticPress options.

This replaces TableCleaner.ts from the TypeScript version.
"""

from sqlalchemy import text

from .config import get_db_connection


class TableCleaner:
    """Cleans StaticPress-specific options from the database before tests."""

    @staticmethod
    def clean() -> None:
        """Clean StaticPress options from wp_options table.

        This replaces the TypeScript version:
        ```typescript
        public static async clean() {
          let connection;
          try {
            const myDataSource = new DataSource(ormconfig);
            connection = await myDataSource.initialize();
            await connection.query("DELETE FROM wp_options WHERE option_name = 'StaticPress::static url'");
            // ...
          } finally {
            if (connection) {
              await connection.destroy();
            }
          }
        }
        ```

        Deletes the following options:
        - StaticPress::static url
        - StaticPress::static dir
        - StaticPress::timeout
        """
        with get_db_connection() as conn:
            # Delete StaticPress configuration options
            conn.execute(text("DELETE FROM wp_options WHERE option_name = 'StaticPress::static url'"))
            conn.execute(text("DELETE FROM wp_options WHERE option_name = 'StaticPress::static dir'"))
            conn.execute(text("DELETE FROM wp_options WHERE option_name = 'StaticPress::timeout'"))
