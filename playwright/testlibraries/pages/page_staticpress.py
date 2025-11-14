"""Page Object Model for StaticPress rebuild page.

This replaces PageStaticPress.ts from the TypeScript version.
"""

from playwright.sync_api import Page


class PageStaticPress:
    """StaticPress plugin rebuild page interactions."""

    def __init__(self, page: Page):
        """Initialize PageStaticPress with a Playwright page.

        Args:
            page: Playwright Page object
        """
        self.page = page

    def click_rebuild(self) -> None:
        """Click the Rebuild button and wait for rebuild to complete.

        This replaces the TypeScript method from PageStaticPress.ts.

        The rebuild process can take up to 3 minutes. This method:
        1. Clicks the "Rebuild" button
        2. Waits for "End" message (timeout: 3 minutes)
        3. Waits for the expected output file to appear in results (timeout: 3 minutes)

        The expected output file path is hardcoded to match the test fixtures:
        /tmp/static/sub/index.html

        Raises:
            TimeoutError: If rebuild doesn't complete within 3 minutes
        """
        self.page.click('input[value="Rebuild"]')

        # Wait for "End" message in #message strong tag (max 3 minutes)
        self.page.locator('xpath=.//p[@id="message"]/strong[text()="End"]').wait_for(
            state="visible",
            timeout=3 * 60 * 1000,
        )

        # Wait for expected result in the result list (max 3 minutes)
        self.page.locator(
            'xpath=.//ul[@class="result-list"]/li[contains(text(), "/tmp/static/sub/index.html")]',
        ).wait_for(state="visible", timeout=3 * 60 * 1000)
