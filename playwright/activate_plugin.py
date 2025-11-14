#!/usr/bin/env python3
"""Activate StaticPress plugin."""

from sqlalchemy import text

from testlibraries.config import get_db_connection

# PHP serialized array with StaticPress2019 plugin
serialized_value = 'a:1:{i:0;s:26:"staticpress2019/plugin.php";}'

with get_db_connection() as conn:
    conn.execute(
        text("UPDATE wp_options SET option_value = :value WHERE option_name = 'active_plugins'"),
        {"value": serialized_value},
    )
    print("Activated StaticPress2019 plugin")
