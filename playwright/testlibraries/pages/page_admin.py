"""Page Object Model for WordPress admin navigation.

This replaces PageAdmin.ts from the TypeScript version.
"""

from playwright.sync_api import Locator
from playwright.sync_api import Page

from ..routine_operation import RoutineOperation


class PageAdmin:
    """WordPress admin menu navigation interactions."""

    def __init__(self, page: Page):
        """Initialize PageAdmin with a Playwright page.

        Args:
            page: Playwright Page object
        """
        self.page = page

    def hover_menu(self, menu: str) -> None:
        """Hover over a main menu item.

        This replaces the TypeScript method from PageAdmin.ts.

        Args:
            menu: Menu text to hover (e.g., "StaticPress2019", "Plugins")
        """
        link_handler_menu = self._get_link_handler_menu(menu)
        # Playwright's hover() already waits for the element to be actionable
        link_handler_menu.hover()

    def click_menu(self, menu: str) -> None:
        """Click a main menu item and wait for page load.

        This replaces the TypeScript method from PageAdmin.ts.

        Args:
            menu: Menu text to click (e.g., "StaticPress2019", "Plugins")
        """
        link_handler = self._get_link_handler_menu(menu)
        link_handler.click()
        self.page.wait_for_load_state("networkidle")

    def wait_for_submenu(self, submenu: str) -> None:
        """Wait for a submenu item to become visible.

        This replaces the TypeScript method from PageAdmin.ts.

        Args:
            submenu: Submenu text to wait for (e.g., "StaticPress2019 Options")
        """
        link_handler = self._get_link_handler_submenu(submenu)
        link_handler.wait_for(state="visible")

    def click_submenu(self, submenu: str) -> None:
        """Click a submenu item and wait for page load.

        This replaces the TypeScript method from PageAdmin.ts.

        Args:
            submenu: Submenu text to click (e.g., "StaticPress2019 Options")
        """
        link_handler = self._get_link_handler_submenu(submenu)
        link_handler.click()
        self.page.wait_for_load_state("networkidle")

    def _get_link_handler_menu(self, menu: str) -> Locator:
        """Get locator for a menu item by text.

        This replaces the private TypeScript method from PageAdmin.ts.

        Uses XPath to find menu items by text content, with proper escaping
        for strings containing quotes.

        Args:
            menu: Menu text

        Returns:
            Playwright Locator for the menu item

        References:
            XPath string escaping:
            https://gist.github.com/tokland/d3bae3b6d3c1576d8700405829bbdb52
        """
        escaped_menu = RoutineOperation.escape_xpath_string(menu)
        xpath = f'//div[@class="wp-menu-name" and contains(text(), {escaped_menu})]'
        return self._get_link_handler(xpath)

    def _get_link_handler_submenu(self, submenu: str) -> Locator:
        """Get locator for a submenu item by exact text match.

        This replaces the private TypeScript method from PageAdmin.ts.

        Args:
            submenu: Submenu text

        Returns:
            Playwright Locator for the submenu item

        References:
            XPath string escaping:
            https://gist.github.com/tokland/d3bae3b6d3c1576d8700405829bbdb52
        """
        escaped_submenu = RoutineOperation.escape_xpath_string(submenu)
        xpath = f"//a[text()={escaped_submenu}]"
        return self._get_link_handler(xpath)

    def _get_link_handler(self, xpath: str) -> Locator:
        """Get first locator matching the given XPath.

        This replaces the private TypeScript method from PageAdmin.ts.

        Args:
            xpath: XPath expression (without xpath= prefix or leading .)

        Returns:
            Playwright Locator for the first matching element
        """
        return self.page.locator(f"xpath=.{xpath}").first
