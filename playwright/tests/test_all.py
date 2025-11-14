"""Main E2E integration test for StaticPress2019.

This replaces __tests__/all.test.ts from the TypeScript version.

Tests:
    - test_sets_option_and_rebuilds: Validates that StaticPress options can be
      set via the admin UI, persisted to the database, and that rebuild
      functionality works correctly.
"""

import os
import re

from playwright.sync_api import Page
from playwright.sync_api import expect
from sqlalchemy import text

from testlibraries.config import get_db_connection
from testlibraries.pages import PageAdmin
from testlibraries.pages import PageLogin
from testlibraries.pages import PageStaticPress
from testlibraries.pages import PageStaticPressOptions

# Configuration constants
# These are also defined in conftest.py and used by fixtures
HOST = os.getenv("HOST", "http://localhost/")
BASIC_AUTH_USERNAME = "authuser"
BASIC_AUTH_PASSWORD = "authpassword"
USERNAME = "test_user"
PASSWORD = "-JfG+L.3-s!A6YmhsKGkGERc+hq&XswU"


def test_sets_option_and_rebuilds(page: Page) -> None:
    """Test that options are set in database and rebuild works.

    This replaces the "sets option and rebuilds" test from the TypeScript
    version in __tests__/all.test.ts (lines 99-152).

    The test:
    1. Logs into WordPress admin
    2. Navigates to StaticPress options page
    3. Sets configuration options (URL, directory, auth, timeout)
    4. Verifies options are saved in database
    5. Navigates to StaticPress rebuild page
    6. Triggers rebuild
    7. Verifies rebuild completes and generates expected output

    Note:
        Option should set into database.
        Home page should dump by rebuild even if basic authentication is enabled.

    Args:
        page: Playwright Page fixture from pytest-playwright.
              Fixtures (setup_wordpress, setup_database_fixtures) run automatically.
    """
    # Step 1: Navigate to WordPress login page and login
    page.goto(HOST + "wp-login.php", wait_until="networkidle")

    # Check if already logged in (WordPress redirects to dashboard)
    if "wp-admin" not in page.url:
        # Need to login
        login_form = page.locator("input#user_login")
        if login_form.is_visible(timeout=5000):
            page_login = PageLogin(page)
            page_login.login(USERNAME, PASSWORD)

    # Handle admin email confirmation prompt (WordPress 5.3+)
    # Navigate directly to admin to bypass the confirmation screen
    if "confirm_admin_email" in page.url:
        page.goto(HOST + "wp-admin/", wait_until="networkidle")

    # Handle database upgrade screen (when WordPress version changes)
    # Note: Database version is now updated via fixture, so this should rarely be needed
    if "upgrade.php" in page.url:
        upgrade_button = page.locator('a.button:has-text("Update WordPress Database")')
        if upgrade_button.count() > 0:
            upgrade_button.click()
            page.wait_for_load_state("networkidle")
        # Navigate to admin after upgrade
        page.goto(HOST + "wp-admin/", wait_until="networkidle")
    elif "wp-admin" not in page.url:
        # If not already on admin page, navigate there
        page.goto(HOST + "wp-admin/", wait_until="networkidle")

    # Check again for upgrade screen after navigation (WordPress might redirect)
    if "upgrade.php" in page.url:
        upgrade_button = page.locator('a.button:has-text("Update WordPress Database")')
        if upgrade_button.count() > 0:
            upgrade_button.click()
            page.wait_for_load_state("networkidle")
        # Navigate to admin after upgrade
        page.goto(HOST + "wp-admin/", wait_until="networkidle")

    # Handle re-authentication if WordPress asks for it (loop to handle multiple redirects)
    max_login_attempts = 3
    login_attempts = 0
    while "wp-login.php" in page.url and login_attempts < max_login_attempts:
        login_attempts += 1
        print(f"Login attempt {login_attempts}, current URL: {page.url}")
        login_form = page.locator("input#user_login")
        try:
            if login_form.is_visible(timeout=2000):
                page_login = PageLogin(page)
                page_login.login(USERNAME, PASSWORD)
                print(f"After login, URL: {page.url}")
        except Exception as e:
            print(f"Login form check failed: {e}")
        # Check if we successfully logged in
        if "wp-admin" not in page.url:
            page.goto(HOST + "wp-admin/", wait_until="networkidle")
            print(f"After navigating to admin, URL: {page.url}")

    # Final debug
    page.screenshot(path="wp46_before_menu_check.png")
    print(f"Final URL before menu check: {page.url}")

    # Step 2: Navigate to StaticPress Options page
    page_admin = PageAdmin(page)
    page_admin.hover_menu("StaticPress2019")
    page_admin.wait_for_submenu("StaticPress2019 Options")
    page_admin.click_submenu("StaticPress2019 Options")

    # Step 3: Set StaticPress options
    page_staticpress_options = PageStaticPressOptions(page)
    static_url = "http://example.com/sub/"
    dump_directory = "/tmp/static/"
    request_timeout = "10"

    page_staticpress_options.set_options(
        static_url,
        dump_directory,
        BASIC_AUTH_USERNAME,
        BASIC_AUTH_PASSWORD,
        request_timeout,
    )

    # Step 4: Verify options are saved in database
    # This replaces the TypeORM connection and queries from TypeScript (lines 119-145)
    with get_db_connection() as conn:
        # Verify static URL
        result = conn.execute(
            text("SELECT option_value FROM wp_options WHERE option_name = :name"),
            {"name": "StaticPress::static url"},
        )
        row = result.fetchone()
        assert row is not None, "StaticPress::static url option not found in database"
        assert row[0] == static_url, f"Static URL mismatch: expected '{static_url}', got '{row[0]}'"

        # Verify dump directory
        result = conn.execute(
            text("SELECT option_value FROM wp_options WHERE option_name = :name"),
            {"name": "StaticPress::static dir"},
        )
        row = result.fetchone()
        assert row is not None, "StaticPress::static dir option not found in database"
        assert row[0] == dump_directory, f"Dump directory mismatch: expected '{dump_directory}', got '{row[0]}'"

        # Verify request timeout
        result = conn.execute(
            text("SELECT option_value FROM wp_options WHERE option_name = :name"),
            {"name": "StaticPress::timeout"},
        )
        row = result.fetchone()
        assert row is not None, "StaticPress::timeout option not found in database"
        assert row[0] == request_timeout, f"Request timeout mismatch: expected '{request_timeout}', got '{row[0]}'"

    # Step 5: Navigate to StaticPress rebuild page
    page_admin.hover_menu("StaticPress2019")
    page_admin.wait_for_submenu("StaticPress2019")
    page_admin.click_submenu("StaticPress2019")

    # Step 6: Trigger rebuild
    page_staticpress = PageStaticPress(page)
    page_staticpress.click_rebuild()

    # Step 7: Verify rebuild output
    # This replaces the Playwright assertion from TypeScript (line 151)
    # Original: await expect(page.locator('li', { hasText: /.*\/tmp\/static\/sub\/index\.html/ })).toBeVisible();
    locator = page.locator("li").filter(has_text=re.compile(r".*/tmp/static/sub/index\.html"))
    expect(locator).to_be_visible()
