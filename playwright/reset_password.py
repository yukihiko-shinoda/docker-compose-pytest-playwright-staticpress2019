#!/usr/bin/env python
"""Reset test_user password to expected value."""

# WordPress password hash for: -JfG+L.3-s!A6YmhsKGkGERc+hq&XswU
# Generated using: wp_hash_password() or password_hash() with PASSWORD_BCRYPT
# For testing, we'll use MD5 (old WordPress format) which still works in 4.6.1
import hashlib

from sqlalchemy import text

from testlibraries.config import get_db_connection

PASSWORD = "-JfG+L.3-s!A6YmhsKGkGERc+hq&XswU"

# Generate WordPress MD5 hash
md5_hash = hashlib.md5(PASSWORD.encode()).hexdigest()
wp_hash = f"$P$B{md5_hash}"  # WordPress uses phpass format

print(f"Password: {PASSWORD}")
print("Attempting to reset password for test_user")

# Actually, let's use WordPress's own password hashing
# For WordPress 4.6.1, we need to use the proper phpass algorithm
# Let's try a known working hash instead

# This is the hash for the password we're using, generated with WordPress 4.6.1
# We'll need to execute PHP to generate it properly, or use a pre-generated one

# For now, let's just check if we can update with a simple hash
with get_db_connection() as conn:
    # First, let's see the current hash
    result = conn.execute(text("SELECT user_pass FROM wp_users WHERE user_login = 'test_user'"))
    row = result.fetchone()
    if row:
        print(f"Current hash: {row[0][:50]}...")

    # WordPress uses phpass hashing. We need to generate the correct hash.
    # Since we can't easily replicate phpass in Python, let's use a different approach:
    # We'll execute a WordPress PHP script to set the password

print("\nNote: Direct password reset requires WordPress phpass implementation.")
print("The password should have been set during WordPress installation in conftest.py")
