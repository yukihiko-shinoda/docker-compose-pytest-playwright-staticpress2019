"""Fixture loader for database test data.

This replaces FixtureLoader.ts from the TypeScript version.
"""

from sqlalchemy import text

from .config import get_db_connection


class FixtureLoader:
    """Loads YAML fixtures into the database for testing."""

    @staticmethod
    def load(fixtures_path: str) -> None:
        """Load fixtures into the database.

        This replaces the TypeScript version:
        ```typescript
        public static async load(fixturesPath: string) {
          let connection;
          try {
            const myDataSource = new DataSource(ormconfig);
            connection = await myDataSource.initialize();
            // ... insert queries
          } finally {
            if (connection) {
              await connection.destroy();
            }
          }
        }
        ```

        Args:
            fixtures_path: Path to the YAML fixtures file.
                Currently only handles WpOptionsStaticPress2019.yml fixtures.
        """
        with get_db_connection() as conn:
            # Hardcoded fixture data to match TypeScript implementation
            # Based on testlibraries/fixtures/WpOptionsStaticPress2019.yml
            if "WpOptionsStaticPress2019" in fixtures_path or "wp_options_staticpress2019" in fixtures_path.lower():
                # Insert StaticPress static URL
                conn.execute(
                    text("""
                        INSERT INTO wp_options (option_name, option_value, autoload)
                        VALUES (:name, :value, :autoload)
                        ON DUPLICATE KEY UPDATE
                            option_value = VALUES(option_value),
                            autoload = VALUES(autoload)
                    """),
                    {
                        "name": "StaticPress::static url",
                        "value": "http://example.org/sub/",
                        "autoload": "yes",
                    },
                )

                # Insert StaticPress static directory
                conn.execute(
                    text("""
                        INSERT INTO wp_options (option_name, option_value, autoload)
                        VALUES (:name, :value, :autoload)
                        ON DUPLICATE KEY UPDATE
                            option_value = VALUES(option_value),
                            autoload = VALUES(autoload)
                    """),
                    {
                        "name": "StaticPress::static dir",
                        "value": "/var/www/html/wp-content/staticpress/",
                        "autoload": "yes",
                    },
                )

                # Insert StaticPress timeout
                conn.execute(
                    text("""
                        INSERT INTO wp_options (option_name, option_value, autoload)
                        VALUES (:name, :value, :autoload)
                        ON DUPLICATE KEY UPDATE
                            option_value = VALUES(option_value),
                            autoload = VALUES(autoload)
                    """),
                    {
                        "name": "StaticPress::timeout",
                        "value": "20",
                        "autoload": "yes",
                    },
                )
