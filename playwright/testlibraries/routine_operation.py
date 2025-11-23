"""Routine operations for Playwright page interactions.

This replaces RoutineOperation.ts from the TypeScript version.
"""

from playwright.sync_api import Page


class RoutineOperation:
    """Utility class for common Playwright operations with XPath helpers."""

    @staticmethod
    def click_by_text(page: Page, tag: str, text: str) -> None:
        """Click an element by tag name and text content.

        This replaces the TypeScript method:
        ```typescript
        public static async clickByText(page: Page, tag: string, text: string): Promise<void> {
          const escapedText = this.escapeXpathString(text);
          const linkHandler = page.locator(`xpath=.//${tag}[contains(text(), ${escapedText})]`).first();
          await linkHandler.click();
        }
        ```

        Args:
            page: Playwright Page object
            tag: HTML tag name (e.g., 'a', 'button', 'div')
            text: Text content to search for

        Example:
            ```python
            RoutineOperation.click_by_text(page, 'a', 'Log In')
            ```

        References:
            XPath string escaping technique:
            https://gist.github.com/tokland/d3bae3b6d3c1576d8700405829bbdb52
        """
        escaped_text = RoutineOperation.escape_xpath_string(text)
        link_handler = page.locator(f"xpath=.//{tag}[contains(text(), {escaped_text})]").first
        link_handler.click()

    @staticmethod
    def escape_xpath_string(text: str) -> str:
        """Escape a string for safe use in XPath expressions.

        This replaces the TypeScript method:
        ```typescript
        public static escapeXpathString(str: string): string {
          const splitedQuotes = str.replace(/'/g, `', "'", '`);
          return `concat('${splitedQuotes}', '')`;
        }
        ```

        This is necessary because XPath 1.0 (used by browsers) doesn't have
        a built-in escaping mechanism for single quotes in string literals.
        The concat() function is used to work around this limitation.

        Args:
            text: String to escape for XPath

        Returns:
            Escaped string safe for use in XPath expressions

        Example:
            ```python
            # Input: "It's a test"
            # Output: concat('It', "'", 's a test', '')
            escaped = RoutineOperation.escape_xpath_string("It's a test")
            ```

        References:
            XPath string escaping technique:
            https://gist.github.com/tokland/d3bae3b6d3c1576d8700405829bbdb52
        """
        # Replace single quotes with ', "'", ' to break the string into parts
        splited_quotes = text.replace("'", "', \"'\", '")
        return f"concat('{splited_quotes}', '')"
