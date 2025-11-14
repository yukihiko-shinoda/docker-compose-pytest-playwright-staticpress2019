#!/usr/bin/env python
"""Debug script to check WordPress admin menu structure."""

import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

HOST = os.getenv("HOST", "http://localhost/")
USERNAME = "test_user"
PASSWORD = "-JfG+L.3-s!A6YmhsKGkGERc+hq&XswU"
BASIC_AUTH_USERNAME = "authuser"
BASIC_AUTH_PASSWORD = "authpassword"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        http_credentials={
            "username": BASIC_AUTH_USERNAME,
            "password": BASIC_AUTH_PASSWORD,
        },
        viewport={"width": 1920, "height": 1080},
    )
    page = context.new_page()

    # Login
    page.goto(HOST + "wp-login.php", wait_until="networkidle")
    page.fill("input#user_login", USERNAME)
    page.fill("input#user_pass", PASSWORD)
    page.click('input[type="submit"][name="wp-submit"]')
    page.wait_for_load_state("networkidle")

    # Take screenshot
    page.screenshot(path="debug_after_login.png")

    # Print page URL and title
    print(f"URL: {page.url}")
    print(f"Title: {page.title()}")

    # Check for StaticPress menu
    menu_items = page.locator("#adminmenu .wp-menu-name").all_text_contents()
    print(f"\nMenu items found: {len(menu_items)}")
    for i, item in enumerate(menu_items):
        print(f"  {i + 1}. {item}")

    # Check if StaticPress2019 is in the menu
    staticpress_menu = page.locator('xpath=.//div[@class="wp-menu-name" and contains(text(), "StaticPress2019")]')
    print(f"\nStaticPress2019 menu count: {staticpress_menu.count()}")

    # Alternative: Check for any menu containing "StaticPress"
    staticpress_any = page.locator("text=StaticPress")
    print(f"Any StaticPress text count: {staticpress_any.count()}")

    # Get full HTML of admin menu for debugging
    menu_html = page.locator("#adminmenu").inner_html()
    with open("admin_menu.html", "w") as f:
        f.write(menu_html)
    print("\nAdmin menu HTML saved to admin_menu.html")

    context.close()
    browser.close()
