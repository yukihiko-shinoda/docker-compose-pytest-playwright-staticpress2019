"""Page Object Model for WordPress login page.

This replaces PageLogin.ts from the TypeScript version.
"""

from playwright.sync_api import Page


class PageLogin:
    """WordPress login page interactions."""

    def __init__(self, page: Page):
        """Initialize PageLogin with a Playwright page.

        Args:
            page: Playwright Page object
        """
        self.page = page

    def login(self, user_name: str, user_password: str) -> None:
        """Log in to WordPress with provided credentials.

        This replaces the TypeScript method:
        ```typescript
        public async login(userName: string, userPassword: string) {
          const usernameInput = this.page.locator('input#user_login');
          const passwordInput = this.page.locator('input#user_pass');
          const loginButton = this.page.locator('input[type="submit"][name="wp-submit"]');

          await usernameInput.waitFor({ state: 'visible' });
          await usernameInput.fill(userName);

          await passwordInput.waitFor({ state: 'visible' });
          await passwordInput.fill(userPassword);

          await loginButton.click();
          await this.page.waitForLoadState('networkidle');
        }
        ```

        Args:
            user_name: WordPress username
            user_password: WordPress password
        """
        username_input = self.page.locator("input#user_login")
        password_input = self.page.locator("input#user_pass")
        login_button = self.page.locator('input[type="submit"][name="wp-submit"]')

        username_input.wait_for(state="visible")
        username_input.fill(user_name)

        password_input.wait_for(state="visible")
        password_input.fill(user_password)

        login_button.click()
        self.page.wait_for_load_state("networkidle")
