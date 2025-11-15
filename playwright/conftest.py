"""Pytest configuration and fixtures for Playwright tests.

This replaces the beforeAll and beforeEach hooks from the TypeScript version in __tests__/all.test.ts.
"""

import os

import pytest
from dotenv import load_dotenv
from passlib.hash import phpass
from playwright.sync_api import Browser
from playwright.sync_api import Page
from sqlalchemy import text

from testlibraries import FixtureLoader
from testlibraries import RoutineOperation
from testlibraries import TableCleaner
from testlibraries.config import get_db_connection
from testlibraries.pages import PageAdmin
from testlibraries.pages import PageLanguageChooser
from testlibraries.pages import PageLogin
from testlibraries.pages import PagePlugins
from testlibraries.pages import PageWelcome

# Load environment variables from .env file
load_dotenv()

# Test configuration constants
# These replace the constants from all.test.ts
HOST = os.getenv("HOST", "http://localhost/")
USERNAME = "test_user"
PASSWORD = "-JfG+L.3-s!A6YmhsKGkGERc+hq&XswU"
BASIC_AUTH_USERNAME = "authuser"
BASIC_AUTH_PASSWORD = "authpassword"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """Configure browser context with HTTP credentials and viewport.

    This replaces the httpCredentials and viewport settings from
    playwright.config.ts.

    Args:
        browser_context_args: Default browser context arguments from pytest-playwright

    Returns:
        Updated browser context arguments
    """
    return {
        **browser_context_args,
        "base_url": HOST,
        "http_credentials": {
            "username": BASIC_AUTH_USERNAME,
            "password": BASIC_AUTH_PASSWORD,
        },
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "test-results/videos",
        "record_video_size": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """Configure browser launch options.

    This replaces the launchOptions from playwright.config.ts.

    Args:
        browser_type_launch_args: Default launch arguments from pytest-playwright

    Returns:
        Updated browser launch arguments
    """
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    return {
        **browser_type_launch_args,
        "args": ["--no-sandbox", "--disable-setuid-sandbox"],
        "headless": headless,
    }


@pytest.fixture(scope="session", autouse=True)
def setup_wordpress(browser: Browser) -> None:
    """One-time setup: Initialize WordPress or login.

    This replaces the test.beforeAll hook from the TypeScript version
    in __tests__/all.test.ts (lines 25-56).

    This fixture runs once per test session and:
    1. Navigates to WordPress (handles basic auth)
    2. Handles language chooser if present (WordPress 5.4.2+)
    3. Either installs WordPress (if welcome page shown) or logs in

    Args:
        browser: Playwright Browser instance from pytest-playwright
    """
    # Ensure test user exists (will trigger reinstall if needed)
    _ensure_test_user_password()

    context = browser.new_context(
        http_credentials={
            "username": BASIC_AUTH_USERNAME,
            "password": BASIC_AUTH_PASSWORD,
        },
        viewport={"width": 1920, "height": 1080},
    )
    page = context.new_page()

    try:
        print("Start basic authentication")
        try:
            page.goto(HOST)
        except Exception as err:
            print(err)
            raise err or Exception("page.goto() failed with empty error")
        print("Finish basic authentication")
        page.screenshot(path="screenshot1.png")

        # From WordPress 5.4.2, language select page is displayed at first
        page_language_chooser = PageLanguageChooser(page)
        if page_language_chooser.is_displayed_now():
            print("Start choose language")
            page_language_chooser.choose("English (United States)")
            print("Finish choose language")

        # Check if WordPress needs installation or login
        page_welcome = PageWelcome(page)
        if page_welcome.is_displayed_now():
            print("Start Initialize")
            _initialize_wordpress(page)
            print("Finish Initialize")
        else:
            print("Start login")
            _login_wordpress(page)
            print("Finish login")
    finally:
        context.close()


def _deactivate_all_plugins() -> None:
    """Deactivate all WordPress plugins by clearing the active_plugins option.

    This can be used to troubleshoot plugin issues or reset plugin state.
    """
    from sqlalchemy import text

    from testlibraries.config import get_db_connection

    # Empty PHP serialized array: a:0:{}
    serialized_value = "a:0:{}"

    with get_db_connection() as conn:
        # Update active_plugins option with empty array
        conn.execute(
            text("UPDATE wp_options SET option_value = :value WHERE option_name = 'active_plugins'"),
            {"value": serialized_value},
        )


def _activate_staticpress_plugin() -> None:
    """Activate StaticPress2019 plugin via database."""
    from sqlalchemy import text

    from testlibraries.config import get_db_connection

    # PHP serialized array with StaticPress2019 plugin
    # a:1:{i:0;s:26:"staticpress2019/plugin.php";}
    serialized_value = 'a:1:{i:0;s:26:"staticpress2019/plugin.php";}'

    with get_db_connection() as conn:
        conn.execute(
            text("UPDATE wp_options SET option_value = :value WHERE option_name = 'active_plugins'"),
            {"value": serialized_value},
        )


def _update_database_version() -> None:
    """Update WordPress database version to match the installed WordPress version.

    This prevents the database upgrade screen from appearing during tests. Detects the WordPress version and sets the
    appropriate db_version.
    """
    from sqlalchemy import text

    from testlibraries.config import get_db_connection

    # Mapping of WordPress versions to their db_version values
    # Based on wp-includes/version.php from each WordPress release
    wp_version_to_db_version = {
        "6.8": "58975",  # WordPress 6.8.x
        "6.7": "58975",  # WordPress 6.7.x
        "6.6": "57155",  # WordPress 6.6.x
        "6.5": "57155",  # WordPress 6.5.x
        "6.4": "57155",  # WordPress 6.4.x
        "6.3": "55853",  # WordPress 6.3.x
        "6.2": "55853",  # WordPress 6.2.x
        "6.1": "53496",  # WordPress 6.1.x
        "6.0": "53496",  # WordPress 6.0.x
        "5.9": "51917",  # WordPress 5.9.x
        "5.8": "49752",  # WordPress 5.8.x
        "5.7": "49752",  # WordPress 5.7.x
        "5.6": "49752",  # WordPress 5.6.x
        "5.5": "48748",  # WordPress 5.5.x
        "5.4": "47018",  # WordPress 5.4.x
        "5.3": "45805",  # WordPress 5.3.x
        "5.2": "44719",  # WordPress 5.2.x
        "5.1": "44719",  # WordPress 5.1.x
        "5.0": "43764",  # WordPress 5.0.x
        "4.9": "38590",  # WordPress 4.9.x
        "4.8": "38590",  # WordPress 4.8.x
        "4.7": "38590",  # WordPress 4.7.x
        "4.6": "38590",  # WordPress 4.6.x
    }

    with get_db_connection() as conn:
        # Get WordPress version from wp_options
        result = conn.execute(text("SELECT option_value FROM wp_options WHERE option_name = 'version'"))
        version_row = result.fetchone()

        if version_row:
            wp_version = version_row[0]
            print(f"WordPress version: {wp_version}")

            # Extract major.minor version (e.g., "6.8" from "6.8.3")
            version_parts = wp_version.split(".")
            major_minor = f"{version_parts[0]}.{version_parts[1]}" if len(version_parts) >= 2 else wp_version

            # Get appropriate db_version
            target_db_version = wp_version_to_db_version.get(major_minor, "58975")  # Default to latest

            # Check current db_version
            result = conn.execute(text("SELECT option_value FROM wp_options WHERE option_name = 'db_version'"))
            db_row = result.fetchone()

            if db_row:
                current_db_version = db_row[0]
                print(f"Current database version: {current_db_version}")

                # Update db_version to match WordPress version
                conn.execute(
                    text("UPDATE wp_options SET option_value = :value WHERE option_name = 'db_version'"),
                    {"value": target_db_version},
                )
                print(f"Updated database version to {target_db_version} (WordPress {major_minor}.x)")
        else:
            print("WordPress version not found in database - skipping db_version update")


def _ensure_test_user_password() -> None:
    """Ensure the test user has the correct password.

    Uses passlib to generate WordPress-compatible password hashes (phpass). If the user exists, updates the password to
    match test expectations. If the wp_users table doesn't exist, does nothing (WordPress needs to be installed first).
    """
    # Generate WordPress-compatible password hash
    # WordPress uses phpass with 8 iteration rounds and 'P' identifier
    password_hash = phpass.using(rounds=8, ident="P").hash(PASSWORD)

    try:
        with get_db_connection() as conn:
            # First check if ANY users exist
            result = conn.execute(text("SELECT COUNT(*) FROM wp_users"))
            total_users = result.fetchone()[0]

            if total_users == 0:
                # No users - database is broken, force WordPress to show installation page
                # by clearing the siteurl option
                conn.execute(
                    text("UPDATE wp_options SET option_value = :value WHERE option_name = 'siteurl'"),
                    {"value": ""},
                )
                print("No users found in database - cleared siteurl to trigger WordPress installation")
                return

            # Check if test_user specifically exists
            result = conn.execute(
                text("SELECT ID FROM wp_users WHERE user_login = :username"),
                {"username": USERNAME},
            )
            user_row = result.fetchone()

            if user_row:
                # User exists - update password to match test expectations
                user_id = user_row[0]
                conn.execute(
                    text("UPDATE wp_users SET user_pass = :password WHERE ID = :user_id"),
                    {"password": password_hash, "user_id": user_id},
                )
                print(f"Updated password for user '{USERNAME}' (ID: {user_id})")
            else:
                print(f"User '{USERNAME}' not found (but other users exist) - login may fail")
    except Exception as e:
        # wp_users table doesn't exist yet - WordPress needs to be installed
        print(f"Cannot check user password - database tables may not exist yet: {e}")
        return


def _initialize_wordpress(page: Page) -> None:
    """Initialize WordPress installation.

    This replaces the initialize() function from the TypeScript version
    in __tests__/all.test.ts (lines 58-71).

    Args:
        page: Playwright Page object
    """
    print("Start Initialize")
    page_welcome = PageWelcome(page)
    page_welcome.install("test_title", USERNAME, PASSWORD, "test@gmail.com")

    RoutineOperation.click_by_text(page, "a", "Log In")
    page.wait_for_load_state("networkidle")

    _login_wordpress(page)

    page_admin = PageAdmin(page)
    page_admin.click_menu("Plugins")

    page_plugins = PagePlugins(page)
    page_plugins.activate_plugin("StaticPress2019")


def _login_wordpress(page: Page) -> None:
    """Login to WordPress.

    This replaces the login() function from the TypeScript version
    in __tests__/all.test.ts (lines 73-77).

    Args:
        page: Playwright Page object
    """
    page.goto(HOST + "wp-login.php", wait_until="networkidle")

    # Check if already logged in (WordPress redirects to dashboard)
    if "wp-admin" in page.url:
        print("Already logged in, skipping login")
        return

    # Check if login form is visible
    login_form = page.locator("input#user_login")
    if not login_form.is_visible(timeout=5000):
        # Already logged in or on a different page
        print("Login form not visible, assuming already logged in")
        return

    page_login = PageLogin(page)
    page_login.login(USERNAME, PASSWORD)


@pytest.fixture(autouse=True)
def setup_database_fixtures() -> None:
    """Setup database fixtures before each test.

    This replaces the test.beforeEach hook from the TypeScript version
    in __tests__/all.test.ts (lines 79-92).

    This fixture runs before every test function and:
    1. Cleans StaticPress options from database
    2. Loads test fixtures from YAML file

    The yield statement allows cleanup code after the test if needed.
    """
    print("Inserting fixtures into the database...")
    try:
        TableCleaner.clean()
    except Exception as err:
        print(err)
        raise err or Exception("TableCleaner.clean() failed with empty error")

    try:
        FixtureLoader.load("./testlibraries/fixtures/WpOptionsStaticPress2019.yml")
        print("Fixtures are successfully loaded.")
    except Exception as err:
        print(err)
        raise err or Exception("FixtureLoader.load() failed with empty error")

    # Ensure StaticPress2019 plugin is activated
    _activate_staticpress_plugin()

    # Update database version to match WordPress version to avoid upgrade screen
    _update_database_version()

    print("Inserted fixtures into the database.")
