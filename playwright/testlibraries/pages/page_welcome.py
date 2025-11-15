"""Page Object Model for WordPress installation welcome page.

This replaces PageWelcome.ts from the TypeScript version.
"""

from playwright.sync_api import Page


class PageWelcome:
    """WordPress installation welcome page interactions."""

    def __init__(self, page: Page):
        """Initialize PageWelcome with a Playwright page.

        Args:
            page: Playwright Page object
        """
        self.page = page

    def install(self, site_title: str, user_name: str, password: str, email: str) -> None:
        """Install WordPress with provided configuration.

        This replaces the TypeScript method from PageWelcome.ts.

        Handles both modern WordPress and legacy WordPress 4.3:
        - Modern: #pass1 for password input
        - Legacy (WordPress 4.3): #pass1-text for password input

        Args:
            site_title: WordPress site title
            user_name: Admin username
            password: Admin password
            email: Admin email address
        """
        self.page.fill('input[id="weblog_title"]', site_title)
        self.page.fill('input[id="user_login"]', user_name)

        # #pass1 is password input on modern WordPress
        # #pass1-text is the one at least on WordPress 4.3
        pass1 = self.page.locator("#pass1")
        pass1_text = self.page.locator("#pass1-text")

        # Check which password field is visible
        try:
            is_pass1_visible = pass1.is_visible()
        except Exception:
            is_pass1_visible = False

        input_password = pass1 if is_pass1_visible else pass1_text

        # Clear the auto-generated password and set our own
        # WordPress auto-generates a password, so we need to clear it first
        input_password.click()
        input_password.press("Control+A")  # Select all text
        input_password.fill(password)
        self.page.fill('input[id="admin_email"]', email)
        self.page.screenshot(path="screenshot.png")

        self.page.click('input[value="Install WordPress"]')
        self.page.wait_for_load_state("networkidle")

    def is_displayed_now(self) -> bool:
        """Check if the WordPress installation welcome page is currently displayed.

        This replaces the TypeScript method from PageWelcome.ts.

        Checks for heading "Information needed" which can be either:
        - <h2> on modern WordPress
        - <h1> at least on WordPress 4.3

        Returns:
            True if welcome page is displayed, False otherwise
        """
        # <h2> is used on modern WordPress, however, <h1> is used at least on WordPress 4.3
        locator = self.page.locator('xpath=.//*[self::h1 or self::h2][text()="Information needed"]')
        return locator.count() > 0
