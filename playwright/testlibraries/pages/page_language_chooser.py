"""Page Object Model for WordPress language chooser page.

This replaces PageLanguageChooser.ts from the TypeScript version.
"""

from playwright.sync_api import Page


class PageLanguageChooser:
    """WordPress language chooser page interactions (WordPress 5.4.2+)."""

    def __init__(self, page: Page):
        """Initialize PageLanguageChooser with a Playwright page.

        Args:
            page: Playwright Page object
        """
        self.page = page

    def choose(self, language: str) -> None:
        """Select a language and continue.

        This replaces the TypeScript method from PageLanguageChooser.ts.

        The language chooser page only appears in WordPress 5.4.2+.

        Args:
            language: Language to select (e.g., "English (United States)")
        """
        self.page.select_option('select[id="language"]', language)

        self.page.click('input[value="Continue"]')
        self.page.wait_for_load_state("networkidle")

    def is_displayed_now(self) -> bool:
        """Check if the language chooser page is currently displayed.

        This replaces the TypeScript method from PageLanguageChooser.ts.

        Returns:
            True if language chooser is displayed, False otherwise
        """
        locator = self.page.locator('xpath=.//label[text()="Select a default language"]')
        return locator.count() > 0
