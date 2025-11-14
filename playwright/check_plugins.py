#!/usr/bin/env python
"""Check which plugins are active in WordPress."""

from sqlalchemy import text

from testlibraries.config import get_db_connection

with get_db_connection() as conn:
    result = conn.execute(text("SELECT option_value FROM wp_options WHERE option_name = 'active_plugins'"))
    row = result.fetchone()
    if row:
        print(f"Active plugins value: {row[0]}")
    else:
        print("No active_plugins option found")
