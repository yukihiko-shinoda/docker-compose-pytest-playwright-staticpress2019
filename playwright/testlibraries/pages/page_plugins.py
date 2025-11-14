"""Page Object Model for WordPress plugins page.

This replaces PagePlugins.ts from the TypeScript version.
"""

from playwright.sync_api import Page

from ..routine_operation import RoutineOperation


class PagePlugins:
    """WordPress plugins page interactions."""

    def __init__(self, page: Page):
        """Initialize PagePlugins with a Playwright page.

        Args:
            page: Playwright Page object
        """
        self.page = page

    def activate_plugin(self, plugin_name: str) -> None:
        """Activate a WordPress plugin by name.

        This replaces the TypeScript method from PagePlugins.ts.

        Uses XPath to find the plugin by name (in a <strong> tag) and then
        clicks the "Activate" link that follows it. If the plugin is already
        active, this method does nothing.

        Args:
            plugin_name: Plugin name as displayed on plugins page
                        (e.g., "StaticPress2019")
        """
        escaped_plugin_name = RoutineOperation.escape_xpath_string(plugin_name)
        xpath = f'//strong[text()={escaped_plugin_name}]/following-sibling::div//a[text()="Activate"]'
        link_handler = self.page.locator(f"xpath=.{xpath}").first

        # Check if the Activate link exists (plugin is not already active)
        if link_handler.count() > 0:
            link_handler.click()
            self.page.wait_for_load_state("domcontentloaded")
