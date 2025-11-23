"""Pytest configuration for unit tests only.

This conftest is used for unit tests that don't require WordPress or browser setup. Unit tests validate code structure,
imports, and basic logic without requiring a live WordPress instance or browser automation.

For integration tests that need WordPress, use the regular conftest.py
"""

import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser
from playwright.sync_api import Page

# Load environment variables
load_dotenv()

# Test configuration constants (same as integration conftest for compatibility)
HOST = os.getenv("HOST", "http://localhost/")
USERNAME = "test_user"
PASSWORD = "-JfG+L.3-s!A6YmhsKGkGERc+hq&XswU"
BASIC_AUTH_USERNAME = "authuser"
BASIC_AUTH_PASSWORD = "authpassword"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """Configure browser context (dummy for unit tests).

    Args:
        browser_context_args: Default browser context args from pytest-playwright

    Returns:
        dict: Browser context configuration
    """
    return {
        **browser_context_args,
        "base_url": HOST,
        "http_credentials": {
            "username": BASIC_AUTH_USERNAME,
            "password": BASIC_AUTH_PASSWORD,
        },
        "viewport": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """Configure browser launch options (dummy for unit tests).

    Args:
        browser_type_launch_args: Default launch args from pytest-playwright

    Returns:
        dict: Browser launch configuration
    """
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    return {
        **browser_type_launch_args,
        "args": ["--no-sandbox", "--disable-setuid-sandbox"],
        "headless": headless,
    }


@pytest.fixture(scope="session", autouse=True)
def setup_wordpress(browser: Browser) -> None:
    """Dummy WordPress setup fixture for unit tests.

    This fixture does nothing - unit tests don't need WordPress.
    The browser fixture is still provided by pytest-playwright but never used.

    Args:
        browser: Playwright Browser instance (unused in unit tests)
    """
    # Skip WordPress setup for unit tests
    print("Skipping WordPress setup for unit tests")


@pytest.fixture(autouse=True)
def setup_database_fixtures() -> None:
    """Dummy database fixture setup for unit tests.

    This fixture does nothing - unit tests don't need database fixtures.
    Integration tests use this to clean and reload database fixtures before each test.
    """
    # Skip database setup for unit tests
    return


def _initialize_wordpress(page: Page) -> None:
    """Dummy helper function for WordPress initialization (unused in unit tests).

    Args:
        page: Playwright Page instance
    """


def _login_wordpress(page: Page) -> None:
    """Dummy helper function for WordPress login (unused in unit tests).

    Args:
        page: Playwright Page instance
    """


@pytest.fixture(scope="session")
def page_classes() -> dict:
    """Fixture providing page object classes for testing.

    Returns:
        dict: Dictionary mapping class names to page object classes
    """
    from testlibraries.pages import PageAdmin
    from testlibraries.pages import PageLanguageChooser
    from testlibraries.pages import PageLogin
    from testlibraries.pages import PagePlugins
    from testlibraries.pages import PageStaticPress
    from testlibraries.pages import PageStaticPressOptions
    from testlibraries.pages import PageWelcome

    return {
        "PageAdmin": PageAdmin,
        "PageLanguageChooser": PageLanguageChooser,
        "PageLogin": PageLogin,
        "PagePlugins": PagePlugins,
        "PageStaticPress": PageStaticPress,
        "PageStaticPressOptions": PageStaticPressOptions,
        "PageWelcome": PageWelcome,
    }
