#!/usr/bin/env python
"""Check WordPress users in database."""

from sqlalchemy import text

from testlibraries.config import get_db_connection

with get_db_connection() as conn:
    result = conn.execute(text("SELECT ID, user_login, user_email FROM wp_users"))
    users = result.fetchall()
    if users:
        print("Users in database:")
        for user in users:
            print(f"  ID: {user[0]}, Login: {user[1]}, Email: {user[2]}")
    else:
        print("No users found in database")
