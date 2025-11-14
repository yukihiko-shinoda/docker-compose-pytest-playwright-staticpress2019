#!/usr/bin/env python
"""Deactivate all WordPress plugins to fix permission errors."""

from sqlalchemy import text

from testlibraries.config import get_db_connection

# Empty PHP serialized array: a:0:{}
serialized_value = "a:0:{}"

with get_db_connection() as conn:
    # Update active_plugins option with empty array
    result = conn.execute(
        text("UPDATE wp_options SET option_value = :value WHERE option_name = 'active_plugins'"),
        {"value": serialized_value},
    )
    print(f"Deactivated all plugins. Rows affected: {result.rowcount}")
