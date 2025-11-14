"""Simple test to validate Python + Playwright setup.

This will be replaced during the full migration.
"""

from playwright.sync_api import Page


def test_playwright_works(page: Page):
    """Basic test to verify Playwright is working."""
    page.goto("https://playwright.dev")
    assert "Playwright" in page.title()
    print("Playwright setup is working correctly!")
