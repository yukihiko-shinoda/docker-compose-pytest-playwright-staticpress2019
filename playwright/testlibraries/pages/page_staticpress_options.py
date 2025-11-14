"""Page Object Model for StaticPress options page.

This replaces PageStaticPressOptions.ts from the TypeScript version.
"""

from playwright.sync_api import Page


class PageStaticPressOptions:
    """StaticPress plugin options page interactions."""

    def __init__(self, page: Page):
        """Initialize PageStaticPressOptions with a Playwright page.

        Args:
            page: Playwright Page object
        """
        self.page = page

    def set_options(
        self,
        static_url: str,
        dump_directory: str,
        basic_authentication_user: str,
        basic_authentication_password: str,
        request_timeout: str,
    ) -> None:
        """Set StaticPress options and save.

        This replaces the TypeScript method from PageStaticPressOptions.ts.

        Args:
            static_url: Static site URL (e.g., "http://example.com/sub/")
            dump_directory: Directory path for static files (e.g., "/tmp/static/")
            basic_authentication_user: HTTP basic auth username
            basic_authentication_password: HTTP basic auth password
            request_timeout: Request timeout in seconds (e.g., "10")
        """
        self._clear_and_type('input[id="static_url"]', static_url)
        self._clear_and_type('input[id="static_dir"]', dump_directory)
        self._clear_and_type('input[id="basic_usr"]', basic_authentication_user)
        self._clear_and_type('input[id="basic_pwd"]', basic_authentication_password)
        self._clear_and_type('input[id="timeout"]', request_timeout)

        self.page.click('input[value="Save Changes"]')
        self.page.wait_for_load_state("domcontentloaded")

    def _clear_and_type(self, css_selector: str, input_text: str) -> None:
        """Clear an input field and type new text.

        This replaces the private TypeScript method from PageStaticPressOptions.ts.

        Uses triple-click to select all existing text before filling.

        Args:
            css_selector: CSS selector for the input element
            input_text: Text to enter
        """
        element_handler = self.page.locator(css_selector)
        element_handler.click(click_count=3)
        element_handler.fill(input_text)
